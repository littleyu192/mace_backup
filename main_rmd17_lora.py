import torch
import os
from torch_geometric.loader import DataLoader
from torch_ema import ExponentialMovingAverage

import logging
import numpy as np
from prettytable import PrettyTable

from config import build_arg_parser
from dataset.PygrMD17 import rMD17
from dataset.Preprocess_rMD17 import rMD17Preprocess
from eval import evaluate
from loss import WeightedEnergyForcesLoss
from train import train
from utils import *
from model.get_model import get_model

from collections import defaultdict


def partially_load_optimizer_by_name(optimizer, checkpoint_state_dict, model):
    old_state = checkpoint_state_dict['state']

    # 当前参数名 -> 参数对象
    current_named_params = dict(model.named_parameters())

    # 当前 optimizer 中的所有 param 对象（必须用这个集合作为主集合）
    optimizer_params = {p for group in optimizer.param_groups for p in group['params']}

    new_state = {}
    matched_names = {}

    for name, p in current_named_params.items():
        if p not in optimizer_params:
            continue  # 🔒 只处理 optimizer 当前管理的 param

        for old_param, state in old_state.items():
            # 用 shape 作为匹配条件（你也可以换成名字完全相同）
            if 'exp_avg' in state and p.shape == state['exp_avg'].shape:
                new_state[p] = state  # ✅ key 是当前 optimizer 的 param 对象
                matched_names[name] = True
                break

    # 保留当前 param_groups，不从 checkpoint 中加载
    compatible_state_dict = {
        'state': new_state,
        'param_groups': optimizer.state_dict()['param_groups']
    }

    optimizer.load_state_dict(compatible_state_dict)

    print(f"✅ Optimizer partially restored: matched {len(matched_names)} parameters.")
    for name in matched_names:
        print(f"  - Restored: {name}")



def safe_partial_load_optimizer(optimizer, checkpoint_state_dict, model):
    old_state = checkpoint_state_dict['state']
    current_named_params = dict(model.named_parameters())

    optimizer_params = {p for group in optimizer.param_groups for p in group['params']}
    new_state = {}
    matched_names = {}

    for name, p in current_named_params.items():
        if p not in optimizer_params:
            continue  # 🔒 只加载 optimizer 已注册的参数

        for old_param, state in old_state.items():
            if 'exp_avg' in state and p.shape == state['exp_avg'].shape:
                new_state[p] = state
                matched_names[name] = True
                break

    compatible_state_dict = {
        'state': new_state,
        'param_groups': optimizer.state_dict()['param_groups']
    }

    optimizer.load_state_dict(compatible_state_dict)

    print(f"✅ Loaded optimizer state for {len(matched_names)} parameters.")
    for name in matched_names:
        print(f"  - Restored: {name}")

def register_missing_params_in_optimizer(optimizer):
    # 当前 optimizer 中注册的所有参数对象
    registered_params = {p for group in optimizer.param_groups for p in group['params']}
    
    # 当前 optimizer.state 中的所有参数
    state_params = set(optimizer.state.keys())
    
    # 找出“幽灵参数”：它们在 state 中但没注册进 param_groups
    missing_params = state_params - registered_params

    if missing_params:
        print(f"🛠️ Registering {len(missing_params)} missing parameters to optimizer.")
        # 添加到新的 param_group 中
        optimizer.add_param_group({'params': list(missing_params)})
    else:
        print("✅ All optimizer state parameters are already registered.")


def main():
    # Setup
    args = build_arg_parser().parse_args()
    setup_seed(args.seed)
    setup_logger(args.output_dir)
    logging.info(f"Configuration: {args}")

    device = (
        torch.device("cuda:" + str(args.device))
        if torch.cuda.is_available()
        else torch.device("cpu")
    )

    # Load data
    train_dataset = rMD17(
        # root="./example/aspirin/data",
        root="./example/Toluene/Toluene/data", 
        name=args.task,
        mode="train" ,
    )
    # split_idx = dataset.get_idx_split(
    #     len(dataset.data.y), valid_fraction=0.05, seed=args.seed
    # )
    valid_dataset = rMD17(
        # root="./example/aspirin/data",
        root="./example/Toluene/Toluene/data",
        name=args.task,
        mode="valid" ,
    )

    train_dataset = rMD17Preprocess(train_dataset, args.cutoff)
    valid_dataset = rMD17Preprocess(valid_dataset, args.cutoff)
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        drop_last=True,
        num_workers=8,
        pin_memory=True,
    )
    valid_loader = DataLoader(
        valid_dataset,
        batch_size=args.val_batch_size,
        shuffle=False,
        drop_last=False,
        num_workers=8,
        pin_memory=True,
    )

    test_dataset = rMD17(
        # root="./example/aspirin/data", 
        root="./example/Toluene/Toluene/data",
        name=args.task, 
        mode="test"
    )
    test_dataset = rMD17Preprocess(test_dataset, args.cutoff)
    test_loader = DataLoader(
        test_dataset,
        batch_size=args.val_batch_size,
        shuffle=False,
        drop_last=False,
        num_workers=8,
    )

    statistics = {
        "z_table": train_dataset.z_table,
        "average_energy": train_dataset.average_energy,
        "avg_num_neighbors": train_dataset.avg_num_neighbors,
        "std": train_dataset.std,
        "mean": train_dataset.mean,
    }
    logging.info(f"Statistics: {statistics}")

    # Build model & optimzer & scheduler
    model = get_model(args, statistics, device)
    logging.info(f"Number of parameters: {count_parameters(model)}")


    optimizer = torch.optim.Adam(
        params=model.parameters(), lr=args.lr, amsgrad=True
    )
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer=optimizer,
        factor=args.lr_factor,
        patience=args.scheduler_patience,
    )



    # Continue run
    if args.continue_run:
        print('\n finetune：\n')

        checkpoint = torch.load(os.path.join('/share/home/zhujie/zhujie/project/PACE/results/pace/Toluene_10000_5/checkpoint.pt'))
        start_epoch = checkpoint["epoch"]

        
        model.load_state_dict(checkpoint["model_state_dict"], strict=False)  # 允许部分加载
        model.to(device)

        # 获取当前模型的参数名称
        current_param_names = set(model.state_dict().keys())

        # 获取检查点中的优化器状态
        checkpoint_optimizer_state = checkpoint["optimizer_state_dict"]

        # 创建过滤后的优化器状态
        filtered_optimizer_state = {"state": {}, "param_groups": []}

        # 复制当前优化器的 param_groups 结构
        current_optimizer_state = optimizer.state_dict()
        filtered_optimizer_state["param_groups"] = current_optimizer_state["param_groups"].copy()

        # 过滤 state，只保留当前模型中存在的参数
        for param_key, param_state in checkpoint_optimizer_state["state"].items():
            if param_key in current_param_names:
                filtered_optimizer_state["state"][param_key] = param_state

        
        # 加载过滤后的优化器状态
        try:
            optimizer.load_state_dict(filtered_optimizer_state)
            print("✅ Successfully loaded partial optimizer state")
        except ValueError as e:
            print("⚠️ Failed to load optimizer state, using default initialization：", e)
            # 如果加载失败，使用默认初始化的优化器
            optimizer = torch.optim.Adam(
                params=model.parameters(), lr=args.lr, amsgrad=True
            )


        if scheduler:
            scheduler.load_state_dict(checkpoint["scheduler_state_dict"])

        lowest_loss = checkpoint["lowest_val_loss"]

        logging.info(f"Loaded model from epoch {start_epoch} from {args.output_dir}")
    else:
        start_epoch = -1

    # EMA & loss
    ema = ExponentialMovingAverage(model.parameters(), decay=0.99)
    loss_fn = WeightedEnergyForcesLoss(
        energy_weight=args.energy_weight, forces_weight=args.force_weight
    )

    ### Training & validation
    logging.info("Started training")
    lowest_loss, valid_loss = np.inf, np.inf
    best_error_e, best_error_f = np.inf, np.inf
    patience_counter = 0
    for epoch in range(1 + start_epoch, args.epochs):
        train_metrics = train(model, train_loader, loss_fn, optimizer, ema, device)

        if epoch % args.eval_interval == 0:
            eval_metrics = evaluate(model, valid_loader, loss_fn, ema, device)
            valid_loss = eval_metrics["loss"]
            error_e = eval_metrics["mae_e"] * 1e3
            error_f = eval_metrics["mae_f"] * 1e3
            lr_cur = optimizer.param_groups[0]["lr"]
            logging.info(
                f"Epoch {epoch}: loss={valid_loss:.4f}, MAE_E={error_e:.2f} meV, MAE_F={error_f:.2f} meV / A, lr_cur={lr_cur:.5f}"
            )

        if epoch % 500 == 0:
            save_checkpoint(
                epoch,
                model,
                optimizer,
                scheduler,
                lowest_loss,
                args.output_dir,
                device,
                ema,
                name="epoch_{}.pt".format(epoch),
            )
        
        save_checkpoint(
            epoch,
            model,
            optimizer,
            scheduler,
            lowest_loss,
            args.output_dir,
            device,
            ema,
        )

    ### Testing
    logging.info("Computing metrics for training, validation, and test sets")

    epoch, _ = load_checkpoint(model, optimizer, scheduler, args.output_dir, device)
    logging.info(f"Loaded model from epoch {epoch}")

    table = PrettyTable()
    table.field_names = [
        "config_type",
        "MAE E / meV",
        "MAE F / meV / A",
    ]
    train_metrics = evaluate(model, train_loader, loss_fn, None, device)
    valid_metrics = evaluate(model, valid_loader, loss_fn, None, device)
    test_metrics = evaluate(model, test_loader, loss_fn, None, device)

    add_row(table, train_metrics, "Train")
    add_row(table, valid_metrics, "Validation")
    add_row(table, test_metrics, "Test")
    logging.info("\n" + str(table))


if __name__ == "__main__":
    main()
