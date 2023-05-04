import tkinter as tk
from tkinter import filedialog
import os

class FileUploader:
    def __init__(self, master):
        self.master = master
        master.title("File Uploader")

        # Create a label and button for selecting files
        self.label = tk.Label(master, text="Select files to upload:")
        self.label.pack()
        self.select_button = tk.Button(master, text="Select", command=self.select_files)
        self.select_button.pack()

    def select_files(self):
        # Open a file dialog to select files
        filenames = filedialog.askopenfilenames()

        # Upload the selected files
        for filename in filenames:
            if filename:
                # Get the base filename (without the path)
                basename = os.path.basename(filename)
                # Set the upload folder
                upload_folder = 'tkupload\Files'
                # Save the file to the upload folder
                with open(os.path.join(upload_folder, basename), 'wb') as f:
                    f.write(open(filename, 'rb').read())

        # Show a message indicating that the files were uploaded
        tk.messagebox.showinfo("Upload Complete", "The selected files were uploaded successfully.")

root = tk.Tk()
app = FileUploader(root)
root.mainloop()
