import os
import shutil
from datetime import datetime
from tkinter import Tk, Button, Label, filedialog, messagebox

"""
File Sorter Project
This script organizes files in a specified directory by their creation date and file extension.

"""
def get_unique_file_name(directory, file_name):
    """Generate a unique file name to avoid overwriting."""
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    new_name = file_name

    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base_name}_{counter}{extension}"
        counter += 1

    return new_name


def gather_all_files(directory):
    """Gather all files from the directory and its subdirectories."""
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
            except Exception as e:
                print(f"Error accessing file {file}: {e}")
    return all_files


def is_already_sorted(file_path, base_directory):
    """Check if a file is already in a YYYY-MM date folder."""
    relative_path = os.path.relpath(file_path, base_directory)
    parts = relative_path.split(os.sep)

    # Check if the file is in a YYYY-MM folder
    if len(parts) >= 2:
        date_folder = parts[0]
        if len(date_folder) == 7 and date_folder[4] == '-' and date_folder[:4].isdigit() and date_folder[5:].isdigit():
            return True  # File is already in a date folder
    return False


def organize_files(directory):
    """Organize files in the specified folder by creation date and then by file extension."""
    if not os.path.exists(directory):
        messagebox.showerror("Error", f"The folder '{directory}' does not exist.")
        return

    # Gather all files from the directory and its subdirectories
    all_files = gather_all_files(directory)

    # Step 1: Organize by creation date (YYYY-MM)
    for file_path in all_files:
        if os.path.isfile(file_path):
            # Check if the file is already sorted
            if is_already_sorted(file_path, directory):
                continue  # Skip files that are already in the correct date folder

            # Get the file name
            file_name = os.path.basename(file_path)

            # Organize by creation date
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(creation_time)
            date_folder_name = creation_date.strftime('%Y-%m')  # Format as YYYY-MM
            date_folder_path = os.path.join(directory, date_folder_name)

            try:
                if not os.path.exists(date_folder_path):
                    os.makedirs(date_folder_path)
            except Exception as e:
                print(f"Error creating directory {date_folder_path}: {e}")
                continue

            # Move the file to the date folder
            try:
                unique_file_name = get_unique_file_name(date_folder_path, file_name)
                date_file_path = os.path.join(date_folder_path, unique_file_name)
                shutil.move(file_path, date_file_path)
            except Exception as e:
                print(f"Error moving file {file_path} to {date_file_path}: {e}")

    # Step 2: Organize each date folder by file extension
    for date_folder in os.listdir(directory):
        date_folder_path = os.path.join(directory, date_folder)

        if os.path.isdir(date_folder_path):
            for file in os.listdir(date_folder_path):
                file_path = os.path.join(date_folder_path, file)

                if os.path.isfile(file_path):
                    # Get the file extension
                    _, extension = os.path.splitext(file)
                    extension = extension[1:]  # Remove the dot from the extension
                    if not extension:
                        extension = "no_extension"  # Handle files without an extension

                    # Create a folder for the extension
                    extension_folder_path = os.path.join(date_folder_path, extension)
                    try:
                        if not os.path.exists(extension_folder_path):
                            os.makedirs(extension_folder_path)
                    except Exception as e:
                        print(f"Error creating directory {extension_folder_path}: {e}")
                        continue

                    # Move the file to the extension folder
                    try:
                        unique_file_name = get_unique_file_name(extension_folder_path, file)
                        extension_file_path = os.path.join(extension_folder_path, unique_file_name)
                        shutil.move(file_path, extension_file_path)
                    except Exception as e:
                        print(f"Error moving file {file_path} to {extension_file_path}: {e}")

    messagebox.showinfo("Success", f"Files in '{directory}' have been organized by creation date and file extension.")


def select_directory():
    """Open a dialog to select a directory and organize files."""
    directory = filedialog.askdirectory(title="Select a Directory to Organize")
    if directory:
        organize_files(directory)


# Main GUI
if __name__ == "__main__":
    root = Tk()
    root.title("File Sorter")
    root.geometry("400x200")

    Label(root, text="Welcome to the File Sorter!", font=("Arial", 14)).pack(pady=10)
    Label(root, text="Click the button below to select a directory to organize.", font=("Arial", 10)).pack(pady=5)

    Button(root, text="Select Directory", command=select_directory, font=("Arial", 12), bg="blue", fg="white").pack(pady=20)

    root.mainloop()