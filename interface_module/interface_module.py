import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Simulated file system
sim_fs = {
    "Root": {
        "Documents": {
            "resume.txt": "This is my resume.",
        },
        "Images": {},
    }
}

class FileManagerApp:
    def init(self, root):
        self.root = root
        self.root.titl("Simulated File Manager")e

        self.tree = ttk.Treeview(root)
        self.tree.pack(side='left', fill='both', expand=True)

        self.text = tk.Text(root, wrap='word')
        self.text.pack(side='right', fill='both', expand=True)

        self.build_tree()

        self.tree.bind("<Double-1>", self.on_open)

    def build_tree(self, parent="", structure=sim_fs):
        for key, val in structure.items():
            node = self.tree.insert(parent, 'end', text=key, open=True)
            if isinstance(val, dict):
                self.build_tree(node, val)

    def on_open(self, event):
        item = self.tree.focus()
        path = self.get_path(item)
        content = self.get_content(sim_fs, path)
        self.text.delete('1.0', tk.END)
        if isinstance(content, str):
            self.text.insert(tk.END, content)
        elif isinstance(content, dict):
            self.text.insert(tk.END, f"Folder: {path[-1]}")
        else:
            self.text.insert(tk.END, "Unknown item")

    def get_path(self, item):
        path = []
        while item:
            path.insert(0, self.tree.item(item)["text"])
            item = self.tree.parent(item)
        return path

    def get_content(self, fs, path):
        for part in path:
            fs = fs.get(part)
            if fs is None:
                return None
        return fs

if _name_ == "_main_":
    root = tk.Tk()
    app = FileManagerApp()
    root.mainloop()
