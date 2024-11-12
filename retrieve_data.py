#!/usr/bin/env python3
from kaggle.api.kaggle_api_extended import KaggleApi
import os
"""
This is a script that simply retrieves data using Kaggle Data Sets through the developers API. It's a simple feature to extracting the data to be used for different types of Machine Learning research or whatever someone needs in the process of using the data as it is something that is shaped and worked on.
"""
# Function to authenticate and download dataset from Kaggle
def download_kaggle_dataset():
    # Ask the user for their Kaggle username and dataset ID affiliated to their kaggle API Token.
    kaggle_username = input("Enter your Kaggle username: ") # Kaggle username for the developer.
    dataset_id = input("Enter the dataset ID (e.g., 'jocelyndumlao/q-and-a-for-admission-of-higher-education-institution'): ") # this is the last part of the authentication process where someone uses the dataset ID which is the username and data set name at the end of the websites address.

    # Set up Kaggle API client
    api = KaggleApi() # this calls on the kaggle API to run the first dataset downlaod function above.
    api.authenticate() # changing 500!

    # Path to save the dataset
    save_path = input("Enter the directory where you want to save the dataset (e.g., 'data'): ") # this is the folder where the data will be stored in order to view the data and extract the data for different use cases in the futere.

    # Ensure the path exists, if not, create it
    if not os.path.exists(save_path):
        os.makedirs(save_path) # creating the file in the current working path of the terminal.
    
    # Download the dataset
    try:
        api.dataset_download_files(dataset_id, path=save_path, unzip=True) 
        print(f"Dataset '{dataset_id}' downloaded successfully to '{save_path}'.") # the format to expressing a successful downlaod. Here the DatasetID and the Path of the downlaod will appear for a successful download.
    except Exception as e:
        print(f"An error occurred while downloading the dataset: {e}") # if the information was not applied correctly or the permissions were not allowed through the Kaggle API.

if __name__ == "__main__":
    download_kaggle_dataset()
    # run the loop of the function

