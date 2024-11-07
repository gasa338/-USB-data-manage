import os
import shutil
import customtkinter
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
from datetime import datetime

progress_row = 4  # Declare progress_row as a global variable


def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    def save_settings():
        selected_drives = drive_listbox.curselection()
        drives_list = [drive_listbox.get(index) for index in selected_drives]
        drives_string = ",".join(drives_list)
        print(drives_string)
        with open("settings.txt", "w") as f:
            f.write(drives_string)
        settings_window.destroy()

    label = tk.Label(settings_window, text="Select Drive(s):")
    label.pack(pady=5)

    drive_listbox = tk.Listbox(settings_window, selectmode=tk.MULTIPLE, width=5, height=5)
    drive_listbox.pack(pady=5)

    def list_drives():
        drive_listbox.delete(0, tk.END)
        # Get a list of all drive letters
        drives = [chr(i) + ':' for i in range(65, 91) if os.path.exists(chr(i) + ':')]
        # Add drives to the listbox
        for drive in drives:
            drive_listbox.insert(tk.END, drive)

    list_drives_button = tk.Button(settings_window, text="List Drives", command=list_drives)
    list_drives_button.pack(pady=5)

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack(pady=5)


def list_drives():
    global progress_row  # Use the global progress_row variable
    # Clear previous list of drives
    drive_listbox.delete(0, tk.END)
    # Get a list of all drive letters
    drives = [chr(i) + ':' for i in range(65, 91) if os.path.exists(chr(i) + ':')]
    # Add drives to the listbox
    for drive in drives:
        drive_listbox.insert(tk.END, drive)


def get_wifi_name_from_settings(file_path):
    wifi_name = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('WIFI_NAME'):
                string_temp = line.split('=')[1].strip()
                substring = string_temp.split('#')
                wifi_name = ''.join(substring[0].split())
                break
    return wifi_name


def select_destination_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        destination_var.set(folder_path)


def get_drive_size(drive):
    try:
        total_size = sum(os.path.getsize(os.path.join(drive, file)) for file in os.listdir(drive) if
                         os.path.isfile(os.path.join(drive, file)))
        size_in_mb = total_size / (1024 * 1024)  # Convert bytes to megabytes
        return f"{size_in_mb:.2f} MB"
    except Exception as e:
        print(f"Error accessing {drive}: {str(e)}")
        return "Unknown"


def copy_from_usb_to_folder(drive, destination_folder, progress_var, status_label, log_text, size_label):
    try:
        # Log start time
        start_time = datetime.now()

        # Initialize copied size
        copied_size = 0

        file_path = os.path.join(drive, 'DCIM', 'MOVIE')

        log_text.insert(tk.END,
                        f"Started copying from {file_path} to {destination_folder} at {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        settings_path = os.path.join(drive, 'SETTING.TXT')

        wifi_name = 'unknown'
        if os.path.isfile(settings_path):
            wifi_name = get_wifi_name_from_settings(settings_path)

        # Get drive size
        drive_size = get_drive_size(file_path)
        size_label.config(text=f"Drive Size: {drive_size}")

        print("file", file_path)
        # List all files and folders in the root directory of the drive
        files = os.listdir(file_path)

        # Calculate total size of files to copy
        total_size = sum(
            os.path.getsize(os.path.join(file_path, file)) for file in files if
            os.path.isfile(os.path.join(file_path, file)))

        if os.path.isdir(file_path):
            destination_dir = os.path.join(destination_folder, wifi_name)
            source_dir = os.listdir(file_path)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            for file in source_dir:
                source_file = os.path.join(file_path, file)
                shutil.copy(source_file, destination_dir)
                copied_size += os.path.getsize(source_file)
                progress = min(int((copied_size / total_size) * 100), 100)
                print(progress)
                progress_var.set(progress)
                log_text.insert(tk.END, f"Copied {source_file} to {destination_folder}\n")
                print(f"Copied {source_file} to {destination_folder}\n")

        # Log end time
        end_time = datetime.now()
        log_text.insert(tk.END,
                        f"Finished copying from {drive} to {destination_folder} at {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_text.insert(tk.END, f"Elapsed time: {end_time - start_time}\n")

        status_label.config(text="Done")
    except Exception as e:
        print(f"Error accessing {drive}: {str(e)}")
        status_label.config(text="Error")


def start_copy():
    global progress_row  # Use the global progress_row variable
    destination_folder = destination_var.get()
    if destination_folder:
        # Get the selected drives from the listbox
        selected_drives = [drive_listbox.get(idx) for idx in drive_listbox.curselection()]

        # Disable the "Start Copy" button
        copy_button.config(state=tk.DISABLED)

        # Create Text widget for logging
        log_text = tk.Text(height=5, width=50, wrap='word')
        log_text.grid(row=20, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')

        # Create Scrollbar widget
        scrollbar = tk.Scrollbar()
        scrollbar.grid(row=20, column=4, sticky='ns')

        # Configure Text widget to use Scrollbar
        log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=log_text.yview)

        # Create progress bars, status labels, and work log for each drive
        for drive in selected_drives:
            progress_var = tk.IntVar()
            progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate",
                                           variable=progress_var)
            progress_bar.grid(row=progress_row, column=1, columnspan=2, padx=5, pady=5)

            status_label = tk.Label(root, text="In Progress")
            status_label.grid(row=progress_row, column=0, padx=5, pady=5)

            size_label = tk.Label(root, text="Drive Size: Calculating...")
            size_label.grid(row=progress_row, column=3, padx=5, pady=5)

            progress_row += 2

            # Start a thread for copying from each drive
            threading.Thread(target=copy_from_usb_to_folder,
                             args=(drive, destination_folder, progress_var, status_label, log_text, size_label)).start()


# Create main window
root = tk.Tk()
root.title("USB Data Copier")

# Destination folder label and entry
destination_label = tk.Label(root, text="Destination Folder:")
destination_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

destination_var = tk.StringVar()
destination_entry = tk.Entry(root, textvariable=destination_var, width=50)
destination_entry.grid(row=0, column=1, padx=5, pady=5)

# Browse button
browse_button = tk.Button(root, text="Browse", command=select_destination_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Listbox to display drives
drive_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=5, height=10)
# drive_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
drive_listbox.grid(row=1, column=0, padx=5, pady=5)

# Button to list drives
list_drives_button = tk.Button(root, text="List Drives", command=list_drives)
list_drives_button.grid(row=1, column=1, pady=10)

# Copy button
copy_button = tk.Button(root, text="Start Copy", command=start_copy)
copy_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a menu
menu = tk.Menu(root)
root.config(menu=menu)

# Create a "File" menu item
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)

# Add a "Settings" menu item
file_menu.add_command(label="Settings", command=open_settings)

root.mainloop()
