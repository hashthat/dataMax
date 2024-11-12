#!/usr/bin/env python3
import os
import difflib
import pandas as pd

"""
This program takes the Kaggle dataset for HBO Max and generates a .txt report. 
The script normalizes the column names, identifies key columns using fuzzy matching, 
and filters top-rated movies based on IMDb ratings. The output is saved to a text file 
for further analysis or machine learning projects.
"""

# Load the HBO Max dataset
try:
    data = pd.read_csv('data.csv')  # This is the file downloaded from the Kaggle dataset.
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'data.csv' not found. Please ensure the file is in the current directory.")
    exit(1)

# Display initial columns
print("Initial Columns:", data.columns)

# Normalize column names
data.columns = data.columns.str.strip().str.lower()
print("Normalized Columns:", data.columns)

# Helper function to find the closest matching column
def find_closest_column(expected_name, columns):
    match = difflib.get_close_matches(expected_name.lower(), [col.lower() for col in columns], n=1, cutoff=0.6)
    return match[0] if match else None

# Find the closest matches for the expected column names
imdb_rating_col = find_closest_column('imdb_rating', data.columns) or 'imdbaveragerating'
genres_col = find_closest_column('genre', data.columns) or 'genres'
release_year_col = find_closest_column('year', data.columns) or 'releaseyear'
available_countries_col = find_closest_column('available_regions', data.columns) or 'availablecountries'
title_col = find_closest_column('title', data.columns) or 'title'

# Print the chosen columns
print(f"Using columns - Title: {title_col}, IMDb Rating: {imdb_rating_col}, Genres: {genres_col}, Year: {release_year_col}, Available Regions: {available_countries_col}")

# Check if the selected columns exist in the DataFrame
missing_cols = [col for col in [title_col, imdb_rating_col, genres_col, release_year_col, available_countries_col] if col not in data.columns]
if missing_cols:
    print(f"Warning: Missing columns in the dataset - {missing_cols}")
    exit(1)

# Convert the IMDb rating column to numeric, handling any non-numeric values
data[imdb_rating_col] = pd.to_numeric(data[imdb_rating_col], errors='coerce')

# Filter for top picks with IMDb rating > 7.5
top_picks = data[data[imdb_rating_col] > 7.5]

# Handle empty top picks
if top_picks.empty:
    print("No movies found with IMDb rating above 7.5.")
    exit(0)

# Sort by IMDb rating in descending order
top_picks = top_picks.sort_values(by=imdb_rating_col, ascending=False)

# Select relevant columns
try:
    top_picks_list = top_picks[[title_col, genres_col, release_year_col, imdb_rating_col, available_countries_col]]
except KeyError as e:
    print(f"Error selecting columns: {e}")
    exit(1)

# Save the top picks to a text file
output_file = 'HBO_Max_Top_Picks.txt'
try:
    with open(output_file, 'w') as file:
        for _, row in top_picks_list.iterrows():
            file.write(f"Title: {row[title_col]}\n")
            file.write(f"Genre: {row[genres_col]}\n")
            file.write(f"Year: {row[release_year_col]}\n")
            file.write(f"IMDb Rating: {row[imdb_rating_col]}\n")
            file.write(f"Available in: {row[available_countries_col]}\n")
            file.write("\n")
    print(f"Top picks saved to {output_file}")
except Exception as e:
    print(f"Error writing to file: {e}")


