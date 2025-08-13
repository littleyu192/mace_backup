import time
import torch
import os

def evaluate(model, loader, loss_fn, ema, device):
    if ema is not None:
        with ema.average_parameters():
            eval_metrics = run_eval(
                model=model,
                loss_fn=loss_fn,
                loader=loader,
                device=device,
            )
    else:
        eval_metrics = run_eval(
            model=model,
            loss_fn=loss_fn,
            loader=loader,
            device=device,
        )

    return eval_metrics


def run_eval(model, loader, loss_fn, device):
    start_time = time.time()
    model.eval()

    total_loss = 0
    delta_es_list, delta_fs_list = [], []
    delta_es_per_atom_list = []

    predicted_energy_batches = []
    predicted_force_batches = []

    for batch in loader:
        batch = batch.to(device)

        output = model(batch, training=False)
        loss = loss_fn(gt_batch=batch, pred=output)

        total_loss += loss.detach().cpu().item()

            # 保存每个 batch 的预测 energy 和 force
        predicted_energy_batches.append(output["energy"].detach().cpu())  # shape: [n_mols, 1]
        if "force" in output:
            predicted_force_batches.append(output["force"].detach().cpu())  # shape: [n_atoms, 3]


        delta_es_list.append(batch.y.detach().cpu() - output["energy"].detach().cpu())
        # delta_es_per_atom_list.append(
        #         ((batch.y - output["energy"]) / (batch.ptr[1:] - batch.ptr[:-1])).detach().cpu()
        #     )
        if "force" in output:
            delta_fs_list.append(
                batch.force.detach().cpu() - output["force"].detach().cpu()
            )
        
        # 指定输出文件路径
        output_dir = "./outputs"
        os.makedirs(output_dir, exist_ok=True)

        energy_file = os.path.join(output_dir, "predicted_energy.txt")
        force_file = os.path.join(output_dir, "predicted_force.txt")

        # 写 energy，每个 batch 一行
        with open(energy_file, "w") as f_energy:
            for batch_energy in predicted_energy_batches:
                # batch_energy shape: [n_mols, 1] → 展平成一维后转为 list
                flat = batch_energy.view(-1).tolist()
                line = " ".join(f"{x:.6f}" for x in flat)
                f_energy.write(line + "\n")

        # 写 force，每个 batch 一行
        with open(force_file, "w") as f_force:
            for batch_force in predicted_force_batches:
                # batch_force shape: [n_atoms, 3] → 展平成一维后转为 list
                flat = batch_force.view(-1).tolist()
                line = " ".join(f"{x:.6f}" for x in flat)
                f_force.write(line + "\n")

    # print('\nE  :\n',predicted_energy_batches)
    # print('\nF  :\n',predicted_force_batches)
    
    delta_es = torch.cat(delta_es_list, dim=0)
    mae_e = torch.mean(torch.abs(delta_es)).item()
    rmse_e = torch.sqrt(torch.mean(torch.square(delta_es))).item()
    # delta_es_per_atom = torch.cat(delta_es_per_atom_list, dim=0)
    # rmse_e_per_atom = torch.sqrt(torch.mean(torch.square(delta_es_per_atom))).item()
    if len(delta_fs_list) > 0:
        delta_fs = torch.cat(delta_fs_list, dim=0)
        mae_f = torch.mean(torch.abs(delta_fs)).item()
        rmse_f = torch.sqrt(torch.mean(torch.square(delta_fs))).item()
    else:
        mae_f = 0
        rmse_f = 0

    
    
    eval_dict = {
        "loss": total_loss / len(loader),
        "mae_e": mae_e,
        "mae_f": mae_f,
        "rmse_e": rmse_e,
        # "rmse_e_per_atom": rmse_e_per_atom,
        "rmse_f": rmse_f,
        "time": time.time() - start_time,
    }

    return eval_dict

















####################################################################################################

####################################################################################################

####################################################################################################


def evaluate1(model, loader, loss_fn, ema, device, name, tag):

    if ema is not None:
        with ema.average_parameters():
            eval_metrics = run_eval1(
                model=model,
                loss_fn=loss_fn,
                loader=loader,
                device=device,
                name=name, tag=tag
            )
    else:
        eval_metrics = run_eval1(
            model=model,
            loss_fn=loss_fn,
            loader=loader,
            device=device,
            name=name, tag=tag
        )

    return eval_metrics


def run_eval1(model, loader, loss_fn, device,  name, tag):
    start_time = time.time()
    model.eval()

    total_loss = 0
    delta_es_list, delta_fs_list = [], []
    delta_es_per_atom_list = []

    predicted_energy_batches = []
    predicted_force_batches = []

    for batch in loader:
        batch = batch.to(device)

        output = model(batch, training=False)
        loss = loss_fn(gt_batch=batch, pred=output)

        total_loss += loss.detach().cpu().item()

            # 保存每个 batch 的预测 energy 和 force
        predicted_energy_batches.append(output["energy"].detach().cpu())  # shape: [n_mols, 1]
        if "force" in output:
            predicted_force_batches.append(output["force"].detach().cpu())  # shape: [n_atoms, 3]


        delta_es_list.append(batch.y.detach().cpu() - output["energy"].detach().cpu())
        # delta_es_per_atom_list.append(
        #         ((batch.y - output["energy"]) / (batch.ptr[1:] - batch.ptr[:-1])).detach().cpu()
        #     )
        if "force" in output:
            delta_fs_list.append(
                batch.force.detach().cpu() - output["force"].detach().cpu()
            )
        
        # 指定输出文件路径
        output_dir = "./outputs"
        os.makedirs(output_dir, exist_ok=True)

        energy_file = os.path.join(output_dir, f"predicted_energy_{name}_{tag}.txt")
        force_file = os.path.join(output_dir, f"predicted_force_{name}_{tag}.txt")

        # 写 energy，每个 batch 一行
        with open(energy_file, "w") as f_energy:
            for batch_energy in predicted_energy_batches:
                # batch_energy shape: [n_mols, 1] → 展平成一维后转为 list
                flat = batch_energy.view(-1).tolist()
                line = " ".join(f"{x:.6f}" for x in flat)
                f_energy.write(line + "\n")

        # 写 force，每个 batch 一行
        with open(force_file, "w") as f_force:
            for batch_force in predicted_force_batches:
                # batch_force shape: [n_atoms, 3] → 展平成一维后转为 list
                flat = batch_force.view(-1).tolist()
                line = " ".join(f"{x:.6f}" for x in flat)
                f_force.write(line + "\n")

    # print('\nE  :\n',predicted_energy_batches)
    # print('\nF  :\n',predicted_force_batches)
    
    delta_es = torch.cat(delta_es_list, dim=0)
    mae_e = torch.mean(torch.abs(delta_es)).item()
    rmse_e = torch.sqrt(torch.mean(torch.square(delta_es))).item()
    # delta_es_per_atom = torch.cat(delta_es_per_atom_list, dim=0)
    # rmse_e_per_atom = torch.sqrt(torch.mean(torch.square(delta_es_per_atom))).item()
    if len(delta_fs_list) > 0:
        delta_fs = torch.cat(delta_fs_list, dim=0)
        mae_f = torch.mean(torch.abs(delta_fs)).item()
        rmse_f = torch.sqrt(torch.mean(torch.square(delta_fs))).item()
    else:
        mae_f = 0
        rmse_f = 0

    
    
    eval_dict = {
        "loss": total_loss / len(loader),
        "mae_e": mae_e,
        "mae_f": mae_f,
        "rmse_e": rmse_e,
        # "rmse_e_per_atom": rmse_e_per_atom,
        "rmse_f": rmse_f,
        "time": time.time() - start_time,
    }

    return eval_dict


