import torch
from torch import nn
from pytorch_ssim import SSIM


class MseSsimLoss(torch.nn.Module):
    def __init__(self):
        super(MseSsimLoss, self).__init__()
        self.mse = nn.MSELoss(reduction='sum')
        self.ssim = SSIM(window_size=5)

    def forward(self, input, target):
        return self.mse(input, target) - self.ssim(input, target)