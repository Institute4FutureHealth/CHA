import torch


class Predictor(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.model = torch.nn.Sequential(
            torch.nn.Linear(12, 12),
            torch.nn.ReLU(),
            torch.nn.Linear(12, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 5),
            torch.nn.ReLU(),
            torch.nn.Linear(5, 5),
            torch.nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.model(x)
        return x
