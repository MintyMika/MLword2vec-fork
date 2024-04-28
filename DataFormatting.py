import json
import os
from alive_progress import alive_bar

'''
This file creates 2 files:
- artistValues.json: a dictionary where the key is the artist name and the value is a unique number
- modifiedPlaylists.txt: a list of playlists where the artist uri is replaced by the unique number no repeated artists
'''


artistDict = dict()
playlists = []

def main():
    global artistDict
    global playlists

    with open('data/artistDict.json') as f:
        artistDict = json.load(f)
    
    # Write to a file a dictionary where the key is the artist name and the value is a unique number

    '''
    Idea: each artist gets a unique number.
    artist_uri: [artist_name, number]

    We want a new dictionary with
    artist_name: unique_number
    '''
    artistDict2 = dict()
    i = 0
    for artist in artistDict:
        artistDict2[artistDict[artist][0]] = i
        i += 1
    with open('data/artistValues.json', 'w') as f:
        json.dump(artistDict2, f)

    modifiedPlaylists = []
    # Change the playlists to use the unique number instead of the artist uri
    with open('data/playlists.json') as f:
        playlists = json.load(f)
        with alive_bar(len(playlists)) as bar:
            for playlist in playlists:
                for i in range(len(playlist)):
                    try:
                        playlist[i] = artistDict2[artistDict[playlist[i]][0]]
                    except:
                        # If the artist is not in the artistDict2, we remove it from the playlist
                        playlist[i] = -1
                # Remove all -1 from the playlist
                playlist = [x for x in playlist if x != -1]

                # Remove duplicates
                playlist = list(set(playlist))
                modifiedPlaylists.append(playlist)
                bar()

    with open('data/modifiedPlaylists.txt', 'w') as f:
        for playlist in modifiedPlaylists:
            # only print the ones that have more than 5 artists
            if len(playlist) > 5:
                f.write(str(playlist) + '\n')




if __name__ == '__main__':
    main()