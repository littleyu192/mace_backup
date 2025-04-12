# set random seed
import torch
torch.manual_seed(42)
import numpy as np
np.random.seed(42)

import os
from copy import deepcopy
from torch_geometric.loader import DataLoader
import sevenn.util as util
from sevenn.nn.scale import SpeciesWiseRescale
from sevenn.train.graph_dataset import SevenNetGraphDataset
from sevenn.train.trainer import Trainer
from sevenn.error_recorder import ErrorRecorder
from sevenn.sevenn_logger import Logger

sevennet_0_cp_path = util.pretrained_name_to_path("7net-0")
model, config = util.model_from_checkpoint(sevennet_0_cp_path)

# To enhance training speed, we will overwrite shift scale module to trainable
# By making energy shift trainable, error quickly converges.
shift_scale_module = model._modules["rescale_atomic_energy"]
shift_scale_module.shift[config['_type_map'][50]] = -35.13398361206055
# shift = shift_scale_module.shift.tolist()
# scale = shift_scale_module.scale.tolist()
# model._modules["rescale_atomic_energy"] = SpeciesWiseRescale(
#     shift=shift,
#     scale=scale,
#     train_shift_scale=True,
# )
print(model)

cutoff = config["cutoff"]  # 7net-0 uses 5.0 Angstrom cutoff
# Preprocess(build graphs) data before training. It will automatically saves processed graph to {root}/sevenn_data/train.pt, metadata + statistics as train.yaml
# If you run below code on more time, it will load saved train.pt automatically instread of rebuilding graph.
# If you have changed your data for some reason, put 'force_reload=True' to reload dataset. Or put processed_name other than

data_path = "data"
working_dir = os.getcwd()  # change if you want
xyz_files = ["train.xyz"]
dataset_files = [os.path.join(data_path, xyz) for xyz in xyz_files]
train_dataset = SevenNetGraphDataset(
    cutoff=cutoff, root=working_dir, files=dataset_files, processed_name="train.pt"
)
xyz_files = ["valid.xyz"]
dataset_files = [os.path.join(data_path, xyz) for xyz in xyz_files]
valid_dataset = SevenNetGraphDataset(
    cutoff=cutoff, root=working_dir, files=dataset_files, processed_name="valid.pt"
)

print(f"# graphs for training: {len(train_dataset)}")
print(f"# graphs for validation: {len(valid_dataset)}")

train_loader = DataLoader(train_dataset, batch_size=5, shuffle=True, num_workers=8)
valid_loader = DataLoader(valid_dataset, batch_size=5)

config.update(
    {
        "optimizer": "adam",
        "optim_param": {"lr": 0.004},
        "scheduler": "linearlr",
        "scheduler_param": {
            "start_factor": 1.0,
            "total_iters": 50,
            "end_factor": 0.0001,
        },
        "is_train_stress": False,
        "is_ddp": False,  # 7net-0 is traied with ddp=True. We override this key False as we won't use it
    }
)
trainer = Trainer.from_config(model, config)

# We have energy, force, stress loss function, which used to train 7net-0.
# We will use it as it is, with loss weight: 1.0, 1.0, and 0.01 for energy, force, and stress, respectively.
print(trainer.loss_functions)
print(trainer.optimizer)
print(trainer.scheduler)

train_recorder = ErrorRecorder.from_config(config)
valid_recorder = deepcopy(train_recorder)
for metric in train_recorder.metrics:
    print(metric)

valid_best = float("inf")
total_epoch = 50

logger = Logger()
logger.screen = True

# As error recorder is long, let's use sevennet_logger for pretty print
# It is similar to outputs when using sevennet with terminal.
with logger:
    logger.greeting()  # prints ascii logo
    for epoch in range(1, total_epoch + 1):  # ~ 16 sec/epoch with RTX4060
        logger.timer_start("epoch")
        logger.writeline(
            f"Epoch {epoch}/{total_epoch}  Learning rate: {trainer.get_lr():.6f}"
        )
        # trainer scans whole data from given loader, and updates error recorder with outputs.
        trainer.run_one_epoch(
            train_loader, is_train=True, error_recorder=train_recorder
        )
        trainer.run_one_epoch(
            valid_loader, is_train=False, error_recorder=valid_recorder
        )
        trainer.scheduler_step()
        train_err = (
            train_recorder.epoch_forward()
        )  # return averaged error over one epoch, then reset.
        valid_err = valid_recorder.epoch_forward()
        logger.bar()
        logger.write_full_table([train_err, valid_err], ["Train", "Valid"])
        logger.timer_end("epoch", message=f"Epoch {epoch} elapsed")

trainer.write_checkpoint(
    os.path.join(working_dir, "checkpoint_fine_tuned.pth"),
    config=config,
    epoch=total_epoch,
)
