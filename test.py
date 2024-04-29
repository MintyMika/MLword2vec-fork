import json
import torch
import torch.nn as nn

# Load the JSON data into a Python dictionary
with open(r'data\artistValues.json', 'r') as f:
    data = json.load(f)

# Function to find the number associated with the given name
def find_number(name):
    if name in data:
        return data[name]
    else:
        return None  # Return None if name not found




matdata = torch.load(r'data\model.pth')

neuralNet = nn.Embedding(num_embeddings=19971, embedding_dim=70)
neuralNet.load_state_dict(torch.load(r'data\model.pth'))
neuralNet.eval()
# Save weights
torch.save(neuralNet.embed.weight, r'data\weights.pth')

artist1 = 24
artist2 = 28
artist3 = 27

# myVec will be the matdata[artist1] + matdata[artist2] + matdata[artist3] and then average
myVec = (matdata[artist1] + matdata[artist2] + matdata[artist3]) / 3

# now matdata * myVec
something = torch.matmul(matdata, myVec)

# divide by sqrt(sum of squares of matdata)
saveLater = torch.norm(matdata, dim=1)

# something / saveLater
cosineSimilarity = torch.div(something, saveLater)

# get the top 10
top10 = torch.topk(cosineSimilarity, 10)

print(top10.indices)
similarArtists = []
for i in top10.indices:
    for key, value in data.items():
        if value == i:
            similarArtists.append(key)
            print(key)