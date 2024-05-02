import torch
import torch.nn as nn


# Define the model architecture
class Artist2Vec(nn.Module):
    def __init__(self, num_embeddings=19971):
        super(Artist2Vec, self).__init__()
        self.embed = nn.Embedding(num_embeddings=num_embeddings, embedding_dim=70)
        self.embed_out = nn.Linear(70, num_embeddings)

    def forward(self, x):
        x = self.embed(x)
        x = torch.mean(x, dim=1)
        x = self.embed_out(x)
        return x

# Load the model
model = Artist2Vec()
model.load_state_dict(torch.load(r'data\model.pth'))
model.eval()

# Extract the weights from the embedding layer
weights = model.embed.weight

# Save the weights
torch.save(weights, 'weights.pth')
