import time
from tqdm import tqdm


def train(model, loader, loss_fn, optimizer, ema, device):
    model.train()

    total_loss = 0
    # for batch in tqdm(loader):
    for batch in loader:
        start_time = time.time()

        batch = batch.to(device)
        optimizer.zero_grad(set_to_none=True)

        output = model(batch, training=True)
        loss = loss_fn(gt_batch=batch, pred=output)
        loss.backward()

        # # 建立参数对象到名字的映射
        # param_to_name = {param: name for name, param in model.named_parameters()}

        # # 遍历优化器中每个参数，查字典拿名字
        # for i, group in enumerate(optimizer.param_groups):
        #     for j, p in enumerate(group['params']):
        #         name = param_to_name.get(p, f"[Group {i}] Param {j} (unnamed)")
        #         if p.grad is not None:
        #             print(f"✅ {name}: grad shape = {p.grad.shape}, grad norm = {p.grad.norm():.4e}")
        #         else:
        #             print(f"❌ {name}: has no grad")



        optimizer.step()

        if ema is not None:
            ema.update()

        total_loss += loss.detach().cpu().item()

    train_dict = {
        "loss": total_loss / len(loader),
        "time": time.time() - start_time,
    }

    return train_dict
