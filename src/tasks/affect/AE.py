import torch


class AE(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(30, 50),
            torch.nn.ReLU(),
            torch.nn.Linear(50, 30),
            torch.nn.ReLU(),
            torch.nn.Linear(30, 24),
            torch.nn.ReLU(),
            torch.nn.Linear(24, 12),
        )

        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(12, 24),
            torch.nn.ReLU(),
            torch.nn.Linear(24, 30),
            torch.nn.ReLU(),
            torch.nn.Linear(30, 50),
            torch.nn.ReLU(),
            torch.nn.Linear(50, 30),
            # torch.nn.Sigmoid()
        )

    def encode(self, x):
        encoded = self.encoder(x)
        return encoded

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
