import json
import numpy as np
import pandas as pd
import os
from alive_progress import alive_bar


# WARNING: This script makes a file that is over 1GB in size don't open that file


artistDict = dict()
playlists = []

def clean_data(file):
    global artistDict
    global playlists
    with open(file) as f:
        data = json.load(f)
        data = data['playlists']

        for playlist in data:
            playlistArtistsURI = []
            for track in playlist['tracks']:
                # Check if artistURI is in the dictionary
                if track['artist_uri'] not in artistDict:
                    artistDict[track['artist_uri']] = [track['artist_name'], 1]
                    # The line below ensures we only keep track of the number of times an artist appears in more than one playlist
                    playlistArtistsURI.append(track['artist_uri'])
                elif track['artist_uri'] in playlistArtistsURI:
                    continue
                else:
                    playlistArtistsURI.append(track['artist_uri'])
                    artistDict[track['artist_uri']][1] += 1

            playlists.append(playlistArtistsURI)

    return



def main():

    #Iterate through all files in the directory
    root_path = r'data\data'
    files = os.listdir(root_path)
    with alive_bar(len(files)) as bar:
        for file in files:
            clean_data(os.path.join(root_path, file))
            bar()
    
    global artistDict
    global playlists

    # Write the artist dict to a file but only the artists that appear in more than 20 playlists
    with open('data/artistDict.json', 'w') as f:
        json.dump({k: v for k, v in artistDict.items() if v[1] > 100}, f)

        artistDict = {k: v for k, v in artistDict.items() if v[1] > 100}
        print(len(artistDict))

    # Write the playlists to a file but only with artists that appear in the artistDict
    with open('data/playlists.json', 'w') as f:
        json.dump([[artist for artist in playlist if artist in artistDict] for playlist in playlists], f)

    return

if __name__ == '__main__':
    main()
                