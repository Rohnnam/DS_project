# File Organizer GUI Implementation
# Gayathri's Role - Interface Builder
# Group 8 - DSA Project

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


# Tree Implementation
class FolderTree:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subfolders = []
        self.files = []
    
    def add_folder(self, folder_name):
        new_folder = FolderTree(folder_name, self)
        self.subfolders.append(new_folder)
        return new_folder
    
    def add_file(self, filename):
        if filename not in self.files:
            self.files.append(filename)
            return True
        return False
    
    def remove_file(self, filename):
        if filename in self.files:
            self.files.remove(filename)
            return True
        return False
    
    def find_folder(self, path):
        """Find folder by path like 'Documents/Projects'"""
        if not path or path == self.name:
            return self
        
        parts = path.split('/')
        current = self
        
        for part in parts:
            found = False
            for subfolder in current.subfolders:
                if subfolder.name == part:
                    current = subfolder
                    found = True
                    break
            if not found:
                return None
        return current
    
    def get_path(self):
        """Get full path from root"""
        if self.parent is None:
            return self.name
        return self.parent.get_path() + "/" + self.name

# Hash Table Implementation
class FileHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.collision_count = 0
    
    def hash_function(self, filename):
        """Simple hash function"""
        total = sum(ord(char) for char in filename.lower())
        return total % self.size
    
    def linear_probe(self, key, attempt):
        """Linear probing: h(k) + i"""
        return (self.hash_function(key) + attempt) % self.size
    
    def insert(self, filename, filepath):
        """Insert file with collision handling"""
        if self.count >= self.size * 0.7:  # Rehash if 70% full
            self.rehash()
        
        attempt = 0
        while attempt < self.size:
            pos = self.linear_probe(filename, attempt)
            
            # If slot is empty, insert here
            if self.table[pos] is None:
                file_info = {
                    'filename': filename,
                    'filepath': filepath,
                    'deleted': False
                }
                self.table[pos] = file_info
                self.count += 1
                if attempt > 0:
                    self.collision_count += 1
                return True
            
            # If same filename, update
            if (self.table[pos] and 
                self.table[pos]['filename'].lower() == filename.lower() and 
                not self.table[pos]['deleted']):
                self.table[pos]['filepath'] = filepath
                return True
            
            attempt += 1
        
        return False  # Table full
    
    def search(self, filename):
        """Search for file"""
        attempt = 0
        while attempt < self.size:
            pos = self.linear_probe(filename, attempt)
            
            if self.table[pos] is None:
                return None
            
            if (self.table[pos]['filename'].lower() == filename.lower() and 
                not self.table[pos]['deleted']):
                return self.table[pos]
            
            attempt += 1
        
        return None
    
    def delete(self, filename):
        """Delete file (lazy deletion)"""
        attempt = 0
        while attempt < self.size:
            pos = self.linear_probe(filename, attempt)
            
            if self.table[pos] is None:
                return False
            
            if (self.table[pos]['filename'].lower() == filename.lower() and 
                not self.table[pos]['deleted']):
                self.table[pos]['deleted'] = True
                self.count -= 1
                return True
            
            attempt += 1
        
        return False
    
    def rehash(self):
        """Rehash when table gets full"""
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        old_count = self.count
        self.count = 0
        self.collision_count = 0
        
        # Reinsert all items
        for item in old_table:
            if item and not item['deleted']:
                self.insert(item['filename'], item['filepath'])

# Main File Organizer Backend
class FileOrganizer:
    def __init__(self):
        self.tree = FolderTree("Root")
        self.hash_table = FileHashTable()
    
    def create_folders(self, path):
        """Create folder structure from path"""
        parts = path.split('/')
        current = self.tree
        
        for part in parts:
            if part:
                found = None
                for subfolder in current.subfolders:
                    if subfolder.name == part:
                        found = subfolder
                        break
                
                if found:
                    current = found
                else:
                    current = current.add_folder(part)
        
        return current
    
    def add_file(self, filename, folder_path=""):
        """Add file to both tree and hash table"""
        if folder_path:
            folder = self.create_folders(folder_path)
        else:
            folder = self.tree
        
        if folder.add_file(filename):
            full_path = folder.get_path() + "/" + filename
            if self.hash_table.insert(filename, full_path):
                return True, f"Added '{filename}' to {folder.get_path()}"
            else:
                folder.remove_file(filename)
                return False, f"Failed to add '{filename}' to hash table"
        else:
            return False, f"File '{filename}' already exists"
    
    def delete_file(self, filename):
        """Delete file from both structures"""
        file_info = self.hash_table.search(filename)
        if not file_info:
            return False, f"File '{filename}' not found"
        
        path_parts = file_info['filepath'].split('/')
        folder_path = '/'.join(path_parts[1:-1])
        
        folder = self.tree.find_folder(folder_path) if folder_path else self.tree
        if folder and folder.remove_file(filename):
            if self.hash_table.delete(filename):
                return True, f"Deleted '{filename}'"
        
        return False, f"Failed to delete '{filename}'"
    
    def search_file(self, filename):
        """Search file using hash table"""
        file_info = self.hash_table.search(filename)
        if file_info:
            return True, f"Found: {filename} at {file_info['filepath']}"
        else:
            return False, f"File '{filename}' not found"

#  GUI Implementation
class FileOrganizerGUI:
    def __init__(self):
        self.organizer = FileOrganizer()
        self.setup_gui()
        self.current_folder = self.organizer.tree
        self.refresh_folder_view()
    
    def setup_gui(self):
        """Initialize the main GUI window"""
        self.root = tk.Tk()
        self.root.title("File Organizer - Group 8")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create main frames
        self.create_header()
        self.create_main_content()
        self.create_buttons()
        self.create_status_bar()
    
    def create_header(self):
        """Create header with title and current path"""
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x", padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📁 File Organizer System", 
                              font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(pady=10)
        
        # Current path display
        path_frame = tk.Frame(header_frame, bg="#2c3e50")
        path_frame.pack(fill="x", padx=10)
        
        tk.Label(path_frame, text="Current Path:", font=("Arial", 10), 
                fg="white", bg="#2c3e50").pack(side="left")
        
        self.path_label = tk.Label(path_frame, text="Root", font=("Arial", 10, "bold"), 
                                  fg="#3498db", bg="#2c3e50")
        self.path_label.pack(side="left", padx=(5, 0))
    
    def create_main_content(self):
        """Create main content area with folder tree and file list"""
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel - Folder tree
        left_frame = tk.LabelFrame(main_frame, text="📂 Folders", 
                                  font=("Arial", 12, "bold"), bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Folder tree with scrollbar
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.folder_tree = ttk.Treeview(tree_frame, selectmode="browse")
        self.folder_tree.heading("#0", text="Folder Structure")
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.folder_tree.yview)
        self.folder_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.folder_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        self.folder_tree.bind("<Double-1>", self.on_folder_select)
        
        # Right panel - Files in current folder
        right_frame = tk.LabelFrame(main_frame, text="📄 Files in Current Folder", 
                                   font=("Arial", 12, "bold"), bg="#f0f0f0")
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # File listbox with scrollbar
        file_frame = tk.Frame(right_frame)
        file_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(file_frame, font=("Arial", 10))
        file_scroll = ttk.Scrollbar(file_frame, orient="vertical", command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=file_scroll.set)
        
        self.file_listbox.pack(side="left", fill="both", expand=True)
        file_scroll.pack(side="right", fill="y")
    
    def create_buttons(self):
        """Create button panel for file operations"""
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # File operations buttons
        file_ops_frame = tk.LabelFrame(button_frame, text="File Operations", 
                                      font=("Arial", 10, "bold"), bg="#f0f0f0")
        file_ops_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        buttons_data = [
            ("➕ Add File", self.add_file, "#27ae60"),
            ("🗑️ Delete File", self.delete_file, "#e74c3c"),
            ("🔍 Search File", self.search_file, "#3498db"),
        ]
        
        for text, command, color in buttons_data:
            btn = tk.Button(file_ops_frame, text=text, command=command, 
                           bg=color, fg="white", font=("Arial", 9, "bold"),
                           padx=10, pady=5, relief="raised", bd=2)
            btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # Folder operations buttons
        folder_ops_frame = tk.LabelFrame(button_frame, text="Folder Operations", 
                                        font=("Arial", 10, "bold"), bg="#f0f0f0")
        folder_ops_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        folder_buttons_data = [
            ("📁 New Folder", self.create_folder, "#f39c12"),
            ("🏠 Go to Root", self.go_to_root, "#9b59b6"),
            ("📊 Show Stats", self.show_stats, "#34495e"),
        ]
        
        for text, command, color in folder_buttons_data:
            btn = tk.Button(folder_ops_frame, text=text, command=command, 
                           bg=color, fg="white", font=("Arial", 9, "bold"),
                           padx=10, pady=5, relief="raised", bd=2)
            btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(self.root, text="Ready", relief="sunken", 
                                  anchor="w", bg="lightgray", font=("Arial", 9))
        self.status_bar.pack(side="bottom", fill="x")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def refresh_folder_tree(self):
        """Refresh the folder tree display"""
        # Clear existing items
        for item in self.folder_tree.get_children():
            self.folder_tree.delete(item)
        
        # Add root and build tree
        self.add_tree_nodes("", self.organizer.tree)
    
    def add_tree_nodes(self, parent, folder):
        """Recursively add nodes to tree"""
        folder_id = self.folder_tree.insert(parent, "end", text=f"📁 {folder.name}", 
                                           values=[folder.get_path()])
        
        for subfolder in folder.subfolders:
            self.add_tree_nodes(folder_id, subfolder)
    
    def refresh_folder_view(self):
        """Refresh both tree and file list"""
        self.refresh_folder_tree()
        self.refresh_file_list()
        self.path_label.config(text=self.current_folder.get_path())
    
    def refresh_file_list(self):
        """Refresh the file list for current folder"""
        self.file_listbox.delete(0, tk.END)
        
        for file in self.current_folder.files:
            self.file_listbox.insert(tk.END, f"📄 {file}")
        
        # Show folder count info
        folder_count = len(self.current_folder.subfolders)
        file_count = len(self.current_folder.files)
        self.update_status(f"Current folder: {folder_count} folders, {file_count} files")
    
    def on_folder_select(self, event):
        """Handle folder selection from tree"""
        selection = self.folder_tree.selection()
        if selection:
            item = self.folder_tree.item(selection[0])
            folder_path = item['values'][0] if item['values'] else "Root"
            
            # Find the folder in our tree structure
            if folder_path == "Root":
                self.current_folder = self.organizer.tree
            else:
                # Remove "Root/" prefix if present
                if folder_path.startswith("Root/"):
                    folder_path = folder_path[5:]
                self.current_folder = self.organizer.tree.find_folder(folder_path)
            
            if self.current_folder:
                self.refresh_folder_view()
    
    def add_file(self):
        """Add a new file dialog"""
        filename = simpledialog.askstring("Add File", "Enter filename:")
        if filename:
            if not self.validate_filename(filename):
                return
            
            folder_path = self.current_folder.get_path()
            if folder_path == "Root":
                folder_path = ""
            else:
                folder_path = folder_path[5:]  # Remove "Root/" prefix
            
            success, message = self.organizer.add_file(filename, folder_path)
            
            if success:
                self.refresh_folder_view()
                messagebox.showinfo("Success", message)
                self.update_status(f"Added file: {filename}")
            else:
                messagebox.showerror("Error", message)
                self.update_status(f"Failed to add file: {filename}")
    
    def delete_file(self):
        """Delete selected file"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file to delete")
            return
        
        filename = self.file_listbox.get(selection[0]).replace("📄 ", "")
        
        result = messagebox.askyesno("Confirm Delete", f"Delete file '{filename}'?")
        if result:
            success, message = self.organizer.delete_file(filename)
            
            if success:
                self.refresh_folder_view()
                messagebox.showinfo("Success", message)
                self.update_status(f"Deleted file: {filename}")
            else:
                messagebox.showerror("Error", message)
                self.update_status(f"Failed to delete file: {filename}")
    
    def search_file(self):
        """Search for a file"""
        filename = simpledialog.askstring("Search File", "Enter filename to search:")
        if filename:
            success, message = self.organizer.search_file(filename)
            
            if success:
                messagebox.showinfo("Search Result", message)
                self.update_status(f"Found: {filename}")
            else:
                messagebox.showwarning("Search Result", message)
                self.update_status(f"Not found: {filename}")
    
    def create_folder(self):
        """Create a new folder"""
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if folder_name:
            if not self.validate_foldername(folder_name):
                return
            
            # Check if folder already exists
            for subfolder in self.current_folder.subfolders:
                if subfolder.name == folder_name:
                    messagebox.showerror("Error", f"Folder '{folder_name}' already exists")
                    return
            
            self.current_folder.add_folder(folder_name)
            self.refresh_folder_view()
            messagebox.showinfo("Success", f"Created folder '{folder_name}'")
            self.update_status(f"Created folder: {folder_name}")
    
    def go_to_root(self):
        """Navigate to root folder"""
        self.current_folder = self.organizer.tree
        self.refresh_folder_view()
        self.update_status("Navigated to Root")
    
    def show_stats(self):
        """Show system statistics"""
        # Count total folders and files
        def count_tree(node):
            folders = 1
            files = len(node.files)
            for subfolder in node.subfolders:
                sub_folders, sub_files = count_tree(subfolder)
                folders += sub_folders
                files += sub_files
            return folders, files
        
        folder_count, file_count = count_tree(self.organizer.tree)
        
        stats_message = f"""System Statistics:
        
📁 Total Folders: {folder_count}
📄 Total Files: {file_count}
🗂️ Hash Table Size: {self.organizer.hash_table.size}
📊 Files in Hash Table: {self.organizer.hash_table.count}
⚡ Load Factor: {self.organizer.hash_table.count/self.organizer.hash_table.size:.2f}
🔄 Collisions: {self.organizer.hash_table.collision_count}
📂 Current Folder: {self.current_folder.get_path()}
        """
        
        messagebox.showinfo("System Statistics", stats_message)
        self.update_status("Displayed system statistics")
    
    def validate_filename(self, filename):
        """Validate filename input"""
        if not filename.strip():
            messagebox.showerror("Invalid Input", "Filename cannot be empty")
            return False
        
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in filename:
                messagebox.showerror("Invalid Input", 
                                   f"Filename cannot contain: {' '.join(invalid_chars)}")
                return False
        
        return True
    
    def validate_foldername(self, foldername):
        """Validate folder name input"""
        if not foldername.strip():
            messagebox.showerror("Invalid Input", "Folder name cannot be empty")
            return False
        
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in foldername:
                messagebox.showerror("Invalid Input", 
                                   f"Folder name cannot contain: {' '.join(invalid_chars)}")
                return False
        
        return True
    
    def load_sample_data(self):
        """Load some sample data for demonstration"""
        # Create sample folder structure
        self.organizer.create_folders("Documents/Assignments")
        self.organizer.create_folders("Documents/Notes")
        self.organizer.create_folders("Pictures/Vacation")
        self.organizer.create_folders("Music/Rock")
        
        # Add sample files
        sample_files = [
            ("project.pdf", "Documents/Assignments"),
            ("homework.docx", "Documents/Assignments"),
            ("notes.txt", "Documents/Notes"),
            ("beach.jpg", "Pictures/Vacation"),
            ("song1.mp3", "Music/Rock")
        ]
        
        for filename, folder_path in sample_files:
            self.organizer.add_file(filename, folder_path)
        
        self.refresh_folder_view()
        self.update_status("Loaded sample data")
    
    def run(self):
        """Start the GUI application"""
        # Load sample data
        self.load_sample_data()
        
        self.update_status("File Organizer ready - Group 8 DSA Project")
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    print("🚀 Starting File Organizer GUI")
    print("Group 8 - DSA Project")
    print("=" * 50)
    
    app = FileOrganizerGUI()
    app.run()
