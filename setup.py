#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import json

"""
This is a script designed for installing the necissary libraries and setting up the Kaggle ID locally in order for the program to work properly. There is the Tkinter, and pandas libraries.
"""
# Function to install libraries
def install_libraries():
    # List of libraries to install
    libraries = ['pandas', 'matplotlib'] 
    # someone could add more libraries here for the setup of other projects. But this ensures the program will run properly
    
    # Install each library using pip
    # This process of using pip utilizes the subprocess library which helps the developer incorporate command line processes.
    for lib in libraries:
        try:
            # Run pip command to install the library
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib]) # checking the executable file.
            messagebox.showinfo("Success", f"{lib} installed successfully!") # sharing the successful install of the library installations.
        except subprocess.CalledProcessError: # houston, we have a problem!
            messagebox.showerror("Error", f"Failed to install {lib}. Please check your environment.")
    
    # tkinter is usually already installed with Python, but we check it separately
    try:
        import tkinter
        messagebox.showinfo("Success", "tkinter is already installed.") # success!
    except ImportError: # this is the exception to try a new subprocess if tkinter is already installed and whether or not there is the need to display an error to tell the user tkinter was unsuccessfully installed.
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinter"])
            messagebox.showinfo("Success", "tkinter installed successfully!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to install tkinter. Please check your environment.") # houston!

# Function to create the kaggle.json file
def create_kaggle_json():
    # Ask the user for their Kaggle username and API token
    username = username_entry.get() # this can be found when token is downloaded on the kaggle website.
    token = token_entry.get() # important for downloading any dataset on kaggle.
    
    # Validate the inputs
    if not username or not token:
        # this keeps the user in the loop to provide both the username and token. They have to match which I had to correct in the process of saving the key.
        messagebox.showerror("Error", "Both username and token must be provided.")
        return
    
    # Ensure the .kaggle directory exists in the user's home directory
    # the .kaggle directory functions alot like an SSH key or even a github key.
    # this is something to look into for future use, github could possibly work the same way as kaggle.
    # I prefer an ssh key.
    home_dir = os.path.expanduser("~") # this is the squiggle of the home directory.
    kaggle_dir = os.path.join(home_dir, '.kaggle') #join the home dir path.
    if not os.path.exists(kaggle_dir): # if the .kaggle directory does not exist, this creates it!
        os.makedirs(kaggle_dir)
    
    # Define the path to the kaggle.json file
    kaggle_json_path = os.path.join(kaggle_dir, 'kaggle.json')
    
    # Create the JSON content
    kaggle_config = {
        "username": username,
        "key": token
    }
    
    # Write the configuration .json file, save it, so we can now use the file path and download the kaggle dataset we choose using the KAggle API and our credentials.
    try:
        with open(kaggle_json_path, 'w') as f:
            json.dump(kaggle_config, f)
        messagebox.showinfo("Success", "Kaggle API credentials saved to kaggle.json")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save kaggle.json: {str(e)}")
    
    # Set the permissions to 600 for the kaggle.json file -- this allows the file to be executable for the API to read the file!
    try:
        os.chmod(kaggle_json_path, 0o600)  # Set read and write permissions for owner only
        messagebox.showinfo("Success", "File permissions set to 600 for kaggle.json")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set file permissions: {str(e)}")

# Function to handle window close
def on_close():
    # Set the permissions to 600 for the kaggle.json file when the window is closed
    # I did this to ensure a working environment for the dataset to be properly downloaded.
    home_dir = os.path.expanduser("~")
    kaggle_json_path = os.path.join(home_dir, '.kaggle', 'kaggle.json')
    if os.path.exists(kaggle_json_path):
        try:
            os.chmod(kaggle_json_path, 0o600)  # Set read and write permissions for owner only
            print("File permissions set to 600 for kaggle.json")
        except Exception as e:
            print(f"Failed to set file permissions: {str(e)}")
    
    root.destroy()  # Close the tkinter window, and chmod the kaggle.json file when closing.

# Creating the main window
# there's the gui for the user input.
def create_gui():
    global username_entry, token_entry
    
    # Create the Tkinter window
    global root
    root = tk.Tk()
    root.title("Library Installer and Kaggle Setup")
    
    # Add a label and entry box for Kaggle Username
    tk.Label(root, text="Kaggle Username:").pack(pady=5)
    username_entry = tk.Entry(root, width=30)
    username_entry.pack(pady=5)
    
    # Add a label and entry box for Kaggle API Token
    tk.Label(root, text="Kaggle API Token:").pack(pady=5)
    token_entry = tk.Entry(root, width=30, show="*")
    token_entry.pack(pady=5) # add some padding to the entry box.
    
    # Add a button to install the libraries
    install_button = tk.Button(root, text="Install Libraries", command=install_libraries, width=20, height=2)
    install_button.pack(pady=20)
    
    # Add a button to create the kaggle.json file in the $PATH
    create_kaggle_button = tk.Button(root, text="Save Kaggle Credentials", command=create_kaggle_json, width=20, height=2)
    create_kaggle_button.pack(pady=10)
    
    # Set window size
    root.geometry("350x300")
    
    # Delete the window when user closes out of the GUI
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Start the GUI
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()

