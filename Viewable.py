import tkinter as tk
from tkinter import messagebox
import json
from test import find_recs
from tkinter import ttk

# Load artist values from artistValues.json
with open(r'data\artistValues.json') as f:
    artist_values = json.load(f)

# Create a list of artist names
artist_names = list(artist_values.keys())

starting_xy = (100, 100)

# Create a Tkinter window
root = tk.Tk()
root.title("Artist Recommendation System")
box_value = tk.StringVar()

combo_boxes = []
list_of_bools = []
check_boxes = []

def search():
    # Change this so it works for all comboboxes
    value_to_search = box_value.get()

    if value_to_search == "" or value_to_search == " ":
        return
    else:
        values_to_display = []
        for artist in artist_names:
            if value_to_search.lower() in artist.lower():
                values_to_display.append(artist)
        
        combo['values'] = values_to_display

def ans():
    # Below is debugging code
    # print(len(combo_boxes))
    # print(len(check_boxes))
    # for i in check_boxes:
    #     print(i.get())

    pos_artists = []
    neg_artists = []
    
    for i in range(len(combo_boxes)):
        if check_boxes[i].get() == 0:
            pos_artists.append(combo_boxes[i].get())
        else:
            neg_artists.append(combo_boxes[i].get())

    

    print(pos_artists)
    print(neg_artists)
    
    artist_recs = find_recs(pos_artists, neg_artists)

    if artist_recs:
        messagebox.showinfo("Recommended Artists", f"Recommended Artists: {', '.join(artist_recs)}")
    else:
        messagebox.showerror("Error", "Artist not found in data")

def add_artist():
    new_var = tk.IntVar()
    new_var.set(0)
    new_check_box = tk.Checkbutton(root, text=None, variable=new_var)
    new_check_box.pack()
    new_check_box.place(x=100, y=100 + 30 * len(check_boxes))
    check_boxes.append(new_var)
    new_string = tk.StringVar()
    new_combo = ttk.Combobox(root, textvariable=new_string)
    new_combo['values'] = artist_names
    new_combo.pack()
    new_combo.place(x=120, y=100 + 30 * len(combo_boxes))
    combo_search_button = tk.Button(root, text="Search", command=search)
    combo_search_button.pack()
    combo_search_button.place(x=270, y=100 + 30 * len(combo_boxes))
    combo_boxes.append(new_combo)


# Make a checkbox for the user to select if they want the artist included or not
var = tk.IntVar()
var.set(0)
check_box = tk.Checkbutton(root, text=None, variable=var)
check_box.pack()
# Make the button in line with the combobox
check_box.place(x=100, y=100)
check_boxes.append(var)

combo = ttk.Combobox(root, textvariable=box_value)
combo['values'] = artist_names
combo.pack()
combo.place(x=120, y=100)
combo_boxes.append(combo)

var = tk.StringVar()
var.set("Search")
search_button = tk.Button(root, textvariable=var, command=search)
search_button.pack()
search_button.place(x=270, y=100)




# Add a button to make another request
add_recommendation = tk.Button(root, text="Add Another Artist", command=add_artist)
add_recommendation.pack()
add_recommendation.place(x=325, y=100)

button = tk.Button(root, text="Submit", command=ans)
button.pack()
button.place(x=250, y=300)
root.mainloop()
