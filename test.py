import json
import torch
import torch.nn as nn

# Load the JSON data into a Python dictionary
with open('artistValues.json', 'r') as f:
    data = json.load(f)

# Function to find the number associated with the given name
def find_number(name):
    if name in data:
        return data[name]
    else:
        return None  # Return None if name not found

#load model
class YourModel(nn.Module):
    def __init__(self):
        super(YourModel, self).__init__()
        # Define your model layers here

    def forward(self, x):
        # Define the forward pass of your model
        return x


name = input("Enter a name: ")
number = find_number(name)
if number is not None:
    # Load the one-hot encoding
    one_hot_vectors = torch.load('OneHot.pt')

    # Specify the index of the vector
    index = number

    # Check if the specified index is within the range of the loaded vectors
    if index < len(one_hot_vectors):
        # Print the one-hot encoding vector at the specified index
        print("One-hot encoding vector at index", index, ":", one_hot_vectors[index])
    else:
        print("Index out of range.")

else:
    print(f"Name '{name}' not found in the data.")

