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

# Create a Tkinter window
root = tk.Tk()
root.title("Artist Recommendation System")
box_value = tk.StringVar()

def search():
    value_to_search = box_value.get()

    if value_to_search == "" or value_to_search == " ":
        return
    else:
        values_to_display = []
        for artist in artist_names:
            if value_to_search.lower() in artist.lower():
                values_to_display.append(artist)
        
        combo['values'] = values_to_display

def another_artist():
    new_combo = ttk.Combobox(root, textvariable=box_value)
    new_combo['values'] = artist_names
    new_combo.pack()

def fun():
    # Get the values from all of the comboboxes
    artist_recs = find_recs(*[box.get() for box in combo.winfo_children()])

    if artist_recs:
        messagebox.showinfo("Recommended Artists", f"Recommended Artists: {', '.join(artist_recs)}")
    else:
        messagebox.showerror("Error", "Artist not found in data")

combo = ttk.Combobox(root, textvariable=box_value)
combo['values'] = artist_names
combo.pack()

var = tk.StringVar()
var.set("Search")
search_button = tk.Button(root, textvariable=var, command=search)
search_button.pack()


# Add a button to make another request
add_recommendation = tk.Button(root, text="Add Another Artist", command=another_artist)
add_recommendation.pack()

button = tk.Button(root, text="Submit", command=fun)
button.pack()

root.mainloop()
