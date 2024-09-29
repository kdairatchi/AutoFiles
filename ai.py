import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class RepositoryBuilder:
    def __init__(self, master):
        self.master = master
        self.master.title("Payload Repository Builder")
        self.master.geometry("500x400")
        self.structure = {}

        self.label = tk.Label(master, text="Payload Repository Structure Builder", font=("Arial", 16))
        self.label.pack(pady=10)

        self.add_folder_button = tk.Button(master, text="Add Folder", command=self.add_folder, width=20)
        self.add_folder_button.pack(pady=5)

        self.add_file_button = tk.Button(master, text="Add File", command=self.add_file, width=20)
        self.add_file_button.pack(pady=5)

        self.generate_button = tk.Button(master, text="Generate Repository", command=self.generate_repository, width=20, bg="green", fg="white")
        self.generate_button.pack(pady=20)

        self.structure_display = tk.Text(master, wrap="word", height=10)
        self.structure_display.pack(padx=10, pady=10)

    def add_folder(self):
        folder_name = simpledialog.askstring("Input", "Enter Folder Name:")
        if folder_name:
            if folder_name not in self.structure:
                self.structure[folder_name] = {}
                self.update_structure_display()
            else:
                messagebox.showwarning("Warning", "Folder already exists.")

    def add_file(self):
        if not self.structure:
            messagebox.showwarning("Warning", "Please add a folder first.")
            return
        folder_name = simpledialog.askstring("Input", "Enter the Folder Name to add the file:")
        if folder_name in self.structure:
            file_name = simpledialog.askstring("Input", "Enter File Name:")
            file_content = simpledialog.askstring("Input", "Enter File Content (optional):")
            if file_name:
                self.structure[folder_name][file_name] = file_content if file_content else ""
                self.update_structure_display()
        else:
            messagebox.showerror("Error", "Folder not found. Please add the folder first.")

    def update_structure_display(self):
        self.structure_display.delete(1.0, tk.END)
        for folder, files in self.structure.items():
            self.structure_display.insert(tk.END, f"Folder: {folder}\n")
            for file, content in files.items():
                self.structure_display.insert(tk.END, f"  ├── File: {file}\n")

    def generate_repository(self):
        base_path = filedialog.askdirectory()
        if not base_path:
            messagebox.showerror("Error", "No directory selected.")
            return

        self.create_repository_structure(base_path, self.structure)
        messagebox.showinfo("Success", f"Repository structure created at: {base_path}")

    def create_repository_structure(self, base_path, structure):
        for folder, files in structure.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for file_name, content in files.items():
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "w") as f:
                    f.write(content)


if __name__ == "__main__":
    root = tk.Tk()
    app = RepositoryBuilder(root)
    root.mainloop()
