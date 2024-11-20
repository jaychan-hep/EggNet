import torch.nn as nn

from .utils.utils import signal_loss, knn_loss, random_loss
from eggnet.utils.timing import time_function


class Contrastive(nn.Module):
    """
    Naive contrastive loss
    """
    def __init__(self, hparams):
        super().__init__()

        self.hparams = hparams

    @time_function
    def forward(self, batch):

        res = {}

        res["signal_loss"] = signal_loss(
            batch,
            self.hparams["margin"],
            node_filter=self.hparams.get("node_filter"),
            weighting_config=self.hparams.get("weighting"),
        )
        res["knn_loss"] = knn_loss(
            batch,
            self.hparams["margin"],
            self.hparams["knn_loss"],
            r=self.hparams.get("r_max"),
            algorithm=self.hparams.get("knn_algorithm", "cu_knn"),
            node_filter=self.hparams.get("node_filter"),
            weighting_config=self.hparams.get("weighting"),
        )
        res["random_loss"] = random_loss(
            batch,
            self.hparams["margin"],
            self.hparams["randomisation"],
            node_filter=self.hparams.get("node_filter"),
            weighting_config=self.hparams.get("weighting"),
        )
        res["loss"] = res["signal_loss"] + res["knn_loss"] + res["random_loss"]

        return res
