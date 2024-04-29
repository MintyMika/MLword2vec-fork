import torch

# Creating 19971 vectors of size 19971 with a one in the index of the artist and then saving them as tensors to a file
vectors = torch.eye(19971)
torch.save(vectors, 'OneHot.pt')

