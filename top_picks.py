#!/usr/bin/env python3
import os
import difflib
import pandas as pd

# Load the HBO Max dataset
data = pd.read_csv('data.csv')
print("Initial Columns:", data.columns)

# Normalize column names
data.columns = data.columns.str.strip().str.lower()
print("Normalized Columns:", data.columns)

# Find the closest matches for the expected column names
imdb_rating_col = difflib.get_close_matches('imdb_rating', data.columns, n=1, cutoff=0.6)
genres_col = difflib.get_close_matches('genre', data.columns, n=1, cutoff=0.6)
release_year_col = difflib.get_close_matches('year', data.columns, n=1, cutoff=0.6)
available_countries_col = difflib.get_close_matches('available_regions', data.columns, n=1, cutoff=0.6)

# Use the found column names or default to known names if not found
imdb_rating_col = imdb_rating_col[0] if imdb_rating_col else 'imdbaveragerating'
genres_col = genres_col[0] if genres_col else 'genres'
release_year_col = release_year_col[0] if release_year_col else 'releaseyear'
available_countries_col = available_countries_col[0] if available_countries_col else 'availablecountries'

print(f"Using columns - IMDb Rating: {imdb_rating_col}, Genres: {genres_col}, Year: {release_year_col}, Available Regions: {available_countries_col}")

# Filter for top picks with IMDb rating > 7.5
top_picks = data[data[imdb_rating_col] > 7.5]

# Sort by IMDb rating in descending order
top_picks = top_picks.sort_values(by=imdb_rating_col, ascending=False)

# Select relevant columns
top_picks_list = top_picks[['title', genres_col, release_year_col, imdb_rating_col, available_countries_col]]

# Save the top picks to a text file
output_file = 'HBO_Max_Top_Picks.txt'
with open(output_file, 'w') as file:
    for _, row in top_picks_list.iterrows():
        file.write(f"Title: {row['title']}\n")
        file.write(f"Genre: {row[genres_col]}\n")
        file.write(f"Year: {row[release_year_col]}\n")
        file.write(f"IMDb Rating: {row[imdb_rating_col]}\n")
        file.write(f"Available in: {row[available_countries_col]}\n")
        file.write("\n")

print(f"Top picks saved to {output_file}")

