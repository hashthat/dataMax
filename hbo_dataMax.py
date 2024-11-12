#!/usr/bin/env python3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# Load and normalize the data
def load_data():
    try:
        # Try to open and read the file to inspect its content
        with open("HBO_Max_Top_Picks.txt", 'r') as file:
            lines = file.readlines()

        # Process the data line by line into a list of dictionaries
        data_list = []
        current_entry = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Title:'):
                if current_entry:
                    data_list.append(current_entry)  # Save the previous entry if it exists
                current_entry = {'title': line[len('Title: '):].strip()}
            elif line.startswith('Genre:'):
                current_entry['genre'] = line[len('Genre: '):].strip()
            elif line.startswith('Year:'):
                current_entry['year'] = line[len('Year: '):].strip()
            elif line.startswith('IMDb Rating:'):
                current_entry['imdb rating'] = line[len('IMDb Rating: '):].strip()
            elif line.startswith('Available in:'):
                current_entry['available regions'] = line[len('Available in: '):].strip()

        # Don't forget to append the last entry
        if current_entry:
            data_list.append(current_entry)

        # Convert list of dictionaries to a DataFrame
        data = pd.DataFrame(data_list)

        # Normalize the column names (strip spaces and convert to lowercase)
        data.columns = data.columns.str.strip().str.lower()

        # Debugging: print columns and the first few rows of data
        print("Columns:", data.columns)
        print(data.head())  # Show the first few rows for validation

        return data
    except FileNotFoundError:
        messagebox.showerror("Error", "File 'HBO_Max_Top_Picks.txt' not found!")
        return pd.DataFrame()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return pd.DataFrame()

# Display data in a table
def display_data():
    data = load_data()
    if data.empty:
        return
    
    # Create a tkinter window to display the data
    window = tk.Tk()
    window.title("HBO Max Top Picks")
    
    # Set up a treeview (table) to show the data
    tree = ttk.Treeview(window, columns=("Title", "Genre", "Year", "IMDb Rating", "Available Regions"), show="headings")
    
    # Define the column headings
    tree.heading("Title", text="Title")
    tree.heading("Genre", text="Genre")
    tree.heading("Year", text="Year")
    tree.heading("IMDb Rating", text="IMDb Rating")
    tree.heading("Available Regions", text="Available Regions")
    
    # Populate the table with data
    for _, row in data.iterrows():
        tree.insert("", "end", values=(row.get('title', 'N/A'), row.get('genre', 'N/A'), row.get('year', 'N/A'),
                                      row.get('imdb rating', 'N/A'), row.get('available regions', 'N/A')))
    
    # Place the treeview in the window and pack it
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Start the tkinter event loop
    window.mainloop()

# Plot IMDb rating histogram
def plot_imdb_histogram():
    data = load_data()
    if data.empty:
        return
    
    fig, ax = plt.subplots()
    ax.hist(data.get('imdb rating', []), bins=10, color='skyblue', edgecolor='black')
    ax.set_title('IMDb Rating Distribution')
    ax.set_xlabel('IMDb Rating')
    ax.set_ylabel('Frequency')
    
    plt.show()

# Plot top genres
def plot_top_genres():
    data = load_data()
    if data.empty:
        return
    
    # Handle genres properly, split and count them
    genres = data.get('genre', '').str.split(', ').explode().value_counts().head(10)
    genres.plot(kind='bar', color='lightcoral')
    plt.title('Top 10 Genres')
    plt.xlabel('Genres')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Plot IMDb Rating vs Year
def plot_rating_vs_year():
    data = load_data()
    if data.empty:
        return
    
    fig, ax = plt.subplots()
    ax.scatter(data.get('year', []), data.get('imdb rating', []), color='darkgreen')
    ax.set_title('IMDb Rating vs Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('IMDb Rating')
    
    plt.show()

# Create GUI window
def create_gui():
    root = tk.Tk()
    root.title("HBO Max Top Picks")

    # Create buttons for different plots
    button1 = tk.Button(root, text="Display Data", command=display_data)
    button1.pack(pady=10)
    
    button2 = tk.Button(root, text="Plot IMDb Histogram", command=plot_imdb_histogram)
    button2.pack(pady=10)
    
    button3 = tk.Button(root, text="Plot Top Genres", command=plot_top_genres)
    button3.pack(pady=10)
    
    button4 = tk.Button(root, text="Plot Rating vs Year", command=plot_rating_vs_year)
    button4.pack(pady=10)

    # Start the tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()

