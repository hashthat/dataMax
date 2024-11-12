#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import json

# Function to install libraries
def install_libraries():
    # List of libraries to install
    libraries = ['pandas', 'matplotlib']
    
    # Install each library using pip
    for lib in libraries:
        try:
            # Run pip command to install the library
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            messagebox.showinfo("Success", f"{lib} installed successfully!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", f"Failed to install {lib}. Please check your environment.")
    
    # tkinter is usually already installed with Python, but we check it separately
    try:
        import tkinter
        messagebox.showinfo("Success", "tkinter is already installed.")
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinter"])
            messagebox.showinfo("Success", "tkinter installed successfully!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to install tkinter. Please check your environment.")

# Function to create the kaggle.json file
def create_kaggle_json():
    # Ask the user for their Kaggle username and API token
    username = username_entry.get()
    token = token_entry.get()
    
    # Validate the inputs
    if not username or not token:
        messagebox.showerror("Error", "Both username and token must be provided.")
        return
    
    # Ensure the .kaggle directory exists in the user's home directory
    home_dir = os.path.expanduser("~")
    kaggle_dir = os.path.join(home_dir, '.kaggle')
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)
    
    # Define the path to the kaggle.json file
    kaggle_json_path = os.path.join(kaggle_dir, 'kaggle.json')
    
    # Create the JSON content
    kaggle_config = {
        "username": username,
        "key": token
    }
    
    # Write the configuration to the kaggle.json file
    try:
        with open(kaggle_json_path, 'w') as f:
            json.dump(kaggle_config, f)
        messagebox.showinfo("Success", "Kaggle API credentials saved to kaggle.json")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save kaggle.json: {str(e)}")
    
    # Set the permissions to 600 for the kaggle.json file
    try:
        os.chmod(kaggle_json_path, 0o600)  # Set read and write permissions for owner only
        messagebox.showinfo("Success", "File permissions set to 600 for kaggle.json")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set file permissions: {str(e)}")

# Function to handle window close
def on_close():
    # Set the permissions to 600 for the kaggle.json file when the window is closed
    home_dir = os.path.expanduser("~")
    kaggle_json_path = os.path.join(home_dir, '.kaggle', 'kaggle.json')
    if os.path.exists(kaggle_json_path):
        try:
            os.chmod(kaggle_json_path, 0o600)  # Set read and write permissions for owner only
            print("File permissions set to 600 for kaggle.json")
        except Exception as e:
            print(f"Failed to set file permissions: {str(e)}")
    
    root.destroy()  # Close the window

# Creating the main window
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
    token_entry.pack(pady=5)
    
    # Add a button to install the libraries
    install_button = tk.Button(root, text="Install Libraries", command=install_libraries, width=20, height=2)
    install_button.pack(pady=20)
    
    # Add a button to create the kaggle.json file
    create_kaggle_button = tk.Button(root, text="Save Kaggle Credentials", command=create_kaggle_json, width=20, height=2)
    create_kaggle_button.pack(pady=10)
    
    # Set the window size
    root.geometry("350x300")
    
    # Handle window close event to set permissions and exit
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Start the GUI
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()

