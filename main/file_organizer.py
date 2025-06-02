# File Organizer Using Trees and Hash Tables
# Group 8 - DSA Project

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
    
    def preorder_traversal(self):
        """Preorder: Root -> Left -> Right"""
        print(f"Folder: {self.get_path()}")
        for subfolder in self.subfolders:
            subfolder.preorder_traversal()
    
    def postorder_traversal(self):
        """Postorder: Left -> Right -> Root"""
        for subfolder in self.subfolders:
            subfolder.postorder_traversal()
        print(f"Folder: {self.get_path()}")
    
    def show_structure(self, indent=""):
        """Display folder hierarchy"""
        print(f"{indent}📁 {self.name}")
        for file in self.files:
            print(f"{indent}  📄 {file}")
        for subfolder in self.subfolders:
            subfolder.show_structure(indent + "  ")

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
    
    def quadratic_probe(self, key, attempt):
        """Quadratic probing: h(k) + i^2"""
        return (self.hash_function(key) + attempt * attempt) % self.size
    
    def insert(self, filename, filepath, probe_type="linear"):
        """Insert file with collision handling"""
        if self.count >= self.size * 0.7:  # Rehash if 70% full
            self.rehash()
        
        attempt = 0
        while attempt < self.size:
            if probe_type == "linear":
                pos = self.linear_probe(filename, attempt)
            else:
                pos = self.quadratic_probe(filename, attempt)
            
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
        print(f"Rehashing from size {self.size} to {self.size * 2}")
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
    
    def show_stats(self):
        """Show hash table statistics"""
        print(f"\nHash Table Stats:")
        print(f"Size: {self.size}")
        print(f"Files stored: {self.count}")
        print(f"Load factor: {self.count/self.size:.2f}")
        print(f"Collisions: {self.collision_count}")

# Main File Organizer (Integration)
class FileOrganizer:
    def __init__(self):
        self.tree = FolderTree("Root")  # tree
        self.hash_table = FileHashTable()  # hash table
        self.current_folder = self.tree
    
    def create_folders(self, path):
        """Create folder structure from path"""
        parts = path.split('/')
        current = self.tree
        
        for part in parts:
            if part:  # Skip empty parts
                # Check if folder already exists
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
        # Find or create the folder
        if folder_path:
            folder = self.create_folders(folder_path)
        else:
            folder = self.current_folder
        
        # Add to tree
        if folder.add_file(filename):
            # Add to hash table
            full_path = folder.get_path() + "/" + filename
            if self.hash_table.insert(filename, full_path):
                print(f"✅ Added '{filename}' to {folder.get_path()}")
                return True
            else:
                folder.remove_file(filename)  # Rollback
                print(f"❌ Failed to add '{filename}' to hash table")
                return False
        else:
            print(f"❌ File '{filename}' already exists")
            return False
    
    def delete_file(self, filename):
        """Delete file from both structures"""
        # Find file in hash table
        file_info = self.hash_table.search(filename)
        if not file_info:
            print(f"❌ File '{filename}' not found")
            return False
        
        # Extract folder path and remove from tree
        path_parts = file_info['filepath'].split('/')
        folder_path = '/'.join(path_parts[1:-1])  # Remove 'Root' and filename
        
        folder = self.tree.find_folder(folder_path) if folder_path else self.tree
        if folder and folder.remove_file(filename):
            if self.hash_table.delete(filename):
                print(f"✅ Deleted '{filename}'")
                return True
        
        print(f"❌ Failed to delete '{filename}'")
        return False
    
    def search_file(self, filename):
        """Search file using hash table"""
        file_info = self.hash_table.search(filename)
        if file_info:
            print(f"🔍 Found: {filename} at {file_info['filepath']}")
            return file_info
        else:
            print(f"❌ File '{filename}' not found")
            return None
    
    def list_folder(self, folder_path=""):
        """List files in a folder"""
        folder = self.tree.find_folder(folder_path) if folder_path else self.tree
        if folder:
            print(f"\n📁 Contents of {folder.get_path()}:")
            print("Folders:")
            for subfolder in folder.subfolders:
                print(f"  📁 {subfolder.name}")
            print("Files:")
            for file in folder.files:
                print(f"  📄 {file}")
        else:
            print(f"❌ Folder '{folder_path}' not found")
    
    def show_tree_structure(self):
        """Display complete folder structure"""
        print("\n🌳 Complete Folder Structure:")
        self.tree.show_structure()
    
    def show_traversals(self):
        """Show tree traversal examples"""
        print("\n📋 Preorder Traversal:")
        self.tree.preorder_traversal()
        
        print("\n📋 Postorder Traversal:")
        self.tree.postorder_traversal()
    
    def show_all_stats(self):
        """Show system statistics"""
        print("\n📊 System Statistics:")
        
        # Count folders and files in tree
        def count_tree(node):
            folders = 1
            files = len(node.files)
            for subfolder in node.subfolders:
                sub_folders, sub_files = count_tree(subfolder)
                folders += sub_folders
                files += sub_files
            return folders, files
        
        folder_count, file_count = count_tree(self.tree)
        print(f"Total Folders: {folder_count}")
        print(f"Total Files: {file_count}")
        
        self.hash_table.show_stats()

# Demo Program
if __name__ == "__main__":
    print("🚀 File Organizer Demo - Group 8")
    print("=" * 40)
    
    # Create file organizer
    organizer = FileOrganizer()
    
    # Create folder structure
    print("\n1. Creating folders...")
    organizer.create_folders("Documents/Assignments")
    organizer.create_folders("Documents/Notes")
    organizer.create_folders("Pictures/Vacation")
    organizer.create_folders("Music/Rock")
    organizer.create_folders("Music/Jazz")
    
    # Add files
    print("\n2. Adding files...")
    organizer.add_file("project.pdf", "Documents/Assignments")
    organizer.add_file("homework.docx", "Documents/Assignments")
    organizer.add_file("notes.txt", "Documents/Notes")
    organizer.add_file("beach.jpg", "Pictures/Vacation")
    organizer.add_file("song1.mp3", "Music/Rock")
    organizer.add_file("jazz1.mp3", "Music/Jazz")
    
    # Test search
    print("\n3. Testing file search...")
    organizer.search_file("project.pdf")
    organizer.search_file("missing.txt")
    
    # Show folder contents
    print("\n4. Listing folder contents...")
    organizer.list_folder("Documents/Assignments")
    
    # Show tree structure
    organizer.show_tree_structure()
    
    # Test tree traversals
    organizer.show_traversals()
    
    # Test file deletion
    print("\n5. Testing file deletion...")
    organizer.delete_file("notes.txt")
    
    # Test hash table collision handling
    print("\n6. Testing collision handling...")
    for i in range(15):
        organizer.add_file(f"test{i}.txt", "Documents")
    
    # Show final statistics
    organizer.show_all_stats()
    
    print("\n✅ Demo completed!")
