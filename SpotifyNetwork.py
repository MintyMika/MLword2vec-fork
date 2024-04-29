import numpy as np
import torch
import re
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch import optim
import time

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")
class SpotifyData(Dataset):
    def __init__(self, filename):
        self.data = []
        with open(filename) as f:
            self.data = [np.array([int(x) for x in re.sub(r"\[|\s|\]", "", line).split(",")]) for line in f]
        self.max = 0
        for playlist in self.data:
            if np.max(playlist) > self.max:
                self.max = np.max(playlist)
        self.len = len(self.data)
        print(self.len)
        print(self.max)

    def __getitem__(self, item):
        sample = np.random.choice(self.data[item], size=5, replace=False)
        return torch.tensor(sample, device=device).long()

    def __len__(self):
        return self.len


class Artist2Vec(nn.Module):
    def __init__(self, num_embeddings=19971):
        super(Artist2Vec, self).__init__()
        self.embed = nn.Embedding(num_embeddings=num_embeddings, embedding_dim=70)
        print(self.embed.weight.shape)
        self.embed_out = nn.Linear(70, num_embeddings)

    def forward(self, x):
        x = self.embed(x)
        x = torch.mean(x, dim=1)
        x = self.embed_out(x)
        return x

# Move data to GPU
sd = SpotifyData("modifiedPlaylists.txt")
dl = DataLoader(sd, batch_size=16, shuffle=True)

# Instantiate model and move it to GPU
model = Artist2Vec().to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

for epochs in range(12):
    running_loss = 0.0
    start_time = time.time()
    for i, data in enumerate(dl, 0):
        input = data[:, 1:].to(device)  # Move input to GPU
        labels = data[:, 0].to(device)   # Move labels to GPU
        optimizer.zero_grad()
        output = model(input)
        loss = loss_fn(output, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    elapsed_time = (time.time() - start_time)/60
    print(f"epoch time:{elapsed_time:.2f} min. Loss: {running_loss}")
