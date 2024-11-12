#!/usr/bin/env python3
from kaggle.api.kaggle_api_extended import KaggleApi
import os
import difflib
import pandas as pd

"""
This script downloads a dataset from Kaggle using the API and then performs analysis on the HBO Max data
to generate a list of top picks based on IMDb ratings.
"""

# Function to authenticate and download dataset from Kaggle
def download_kaggle_dataset():
    # Ask the user for their Kaggle username and dataset ID
    kaggle_username = input("Enter your Kaggle username: ")
    dataset_id = input("Enter the dataset ID (e.g., 'bricevergnou/spotify-recommendation'): ")

    # Set up Kaggle API client
    api = KaggleApi()
    api.authenticate()

    # Path to save the dataset
    save_path = input("Enter the directory where you want to save the dataset (e.g., 'data'): ")

    # Ensure the path exists, if not, create it
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Download the dataset
    try:
        api.dataset_download_files(dataset_id, path=save_path, unzip=True)
        print(f"Dataset '{dataset_id}' downloaded successfully to '{save_path}'.")
    except Exception as e:
        print(f"An error occurred while downloading the dataset: {e}")
        return None

    # Return the path of the downloaded file
    return os.path.join(save_path, 'data.csv')

# Function to analyze HBO Max data and generate top picks
def analyze_hbo_data(file_path):
    if not os.path.exists(file_path):
        print(f"Data file '{file_path}' not found.")
        return

    # Load the dataset
    data = pd.read_csv(file_path)
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
    try:
        top_picks = data[data[imdb_rating_col] > 7.5]
    except KeyError:
        print("Error: IMDb rating column not found. Please check the dataset.")
        return

    # Sort by IMDb rating in descending order
    top_picks = top_picks.sort_values(by=imdb_rating_col, ascending=False)

    # Select relevant columns
    try:
        top_picks_list = top_picks[['title', genres_col, release_year_col, imdb_rating_col, available_countries_col]]
    except KeyError as e:
        print(f"Error: {e}. One of the required columns is missing.")
        return

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

if __name__ == "__main__":
    # Download dataset
    csv_file_path = download_kaggle_dataset()

    # Analyze the data if the download was successful
    if csv_file_path:
        analyze_hbo_data(csv_file_path)

