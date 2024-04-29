import torch

# Creating 19970 vectors of size 19970 with a one in the index of the artist and then saving them as tensors to a file
vectors = torch.eye(19970)
# print(vectors[2])
torch.save(vectors, 'OneHot.pt')

