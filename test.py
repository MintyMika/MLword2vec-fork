import json
import torch
import torch.nn as nn

#Load in weights
matdata = torch.load(r'weightsD.pth')


# Load the JSON data into a Python dictionary
with open(r'data\artistValues.json', 'r') as f:
    data = json.load(f)

# Function to find the number associated with the given name
def find_number(name):
    if name in data:
        return data[name]
    else:
        return None  # Return None if name not found

#Function to find 10 recommended artists
def find_recs(*artists):
    artist_numbers = [find_number(artist) for artist in artists]

    if None in artist_numbers:
        missing_artists = [artists[i] for i, number in enumerate(artist_numbers) if number is None]
        print(f"The following artist(s) could not be found in the data: {', '.join(missing_artists)}")
        return

    # myVec will be the matdata[artist1] + matdata[artist2] + matdata[artist3] ... + matdata[artistn] and then average
    myVec = torch.mean(torch.stack([matdata[artist] for artist in artist_numbers]), dim=0)

    # now matdata * myVec
    something = torch.matmul(matdata, myVec)

    # divide by sqrt(sum of squares of matdata)
    saveLater = torch.norm(matdata, dim=1)

    # something / saveLater
    cosineSimilarity = torch.div(something, saveLater)

    # get the top 13
    top13 = torch.topk(cosineSimilarity, 13)

    # Convert indices tensor to a list
    top13_indices = top13.indices.tolist()

    # Filter out the indices corresponding to input artists
    filtered_indices = [index for index in top13_indices if index not in artist_numbers]

    # Print and store similar artists excluding input artists
    similarArtists = []
    for i in filtered_indices[:10]:  # Take the first 10 remaining artists
        for key, value in data.items():
            if value == i:
                similarArtists.append(key)
                print(key)

    return similarArtists


artist1 = input("Enter an artist name: ")
artist2 = input("Enter an artist name: ")
artist3 = input("Enter an artist name: ")

find_recs(artist1, artist2, artist3)
