class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subfolders = []
        self.files = []  # Store files in this folder
    
    # Add a subfolder
    def add_subfolder(self, folder_name):
        new_folder = Folder(folder_name, parent=self)
        self.subfolders.append(new_folder)
        return new_folder
    
    # Remove a subfolder
    def remove_subfolder(self, folder_name):
        for i, subfolder in enumerate(self.subfolders):
            if subfolder.name == folder_name:
                del self.subfolders[i]
                return True
        return False
    
    # Add file to folder
    def add_file(self, filename):
        if filename not in self.files:
            self.files.append(filename)
            return True
        return False
    
    # Remove file from folder
    def remove_file(self, filename):
        if filename in self.files:
            self.files.remove(filename)
            return True
        return False
    
    # Find a folder by name (DFS traversal)
    def find_folder(self, folder_name):
        if self.name == folder_name:
            return self
        
        for subfolder in self.subfolders:
            result = subfolder.find_folder(folder_name)
            if result:
                return result
        return None
    
    # Get full path from root
    def get_path(self):
        if self.parent is None:
            return self.name
        return self.parent.get_path() + "/" + self.name
    
    # Preorder traversal (Root -> Left -> Right)
    def preorder_traversal(self, visit_func=None):
        if visit_func:
            visit_func(self)
        else:
            print(f"Visiting: {self.get_path()}")
        
        for subfolder in self.subfolders:
            subfolder.preorder_traversal(visit_func)
    
    # Postorder traversal (Left -> Right -> Root)
    def postorder_traversal(self, visit_func=None):
        for subfolder in self.subfolders:
            subfolder.postorder_traversal(visit_func)
        
        if visit_func:
            visit_func(self)
        else:
            print(f"Visiting: {self.get_path()}")
    
    # Level-order traversal (BFS)
    def level_order_traversal(self):
        queue = [self]
        while queue:
            current = queue.pop(0)
            print(f"Level {self._get_depth(current)}: {current.get_path()}")
            queue.extend(current.subfolders)
    
    def _get_depth(self, node):
        depth = 0
        while node.parent:
            depth += 1
            node = node.parent
        return depth
    
    # Print the folder hierarchy with files
    def print_hierarchy(self, indent="", show_files=True):
        print(f"{indent}📁 {self.name}")
        
        if show_files and self.files:
            for file in self.files:
                print(f"{indent}    📄 {file}")
        
        for sub in self.subfolders:
            sub.print_hierarchy(indent + "    ", show_files)
    
    # Count total folders and files
    def get_statistics(self):
        folder_count = 1  # Count self
        file_count = len(self.files)
        
        for subfolder in self.subfolders:
            sub_stats = subfolder.get_statistics()
            folder_count += sub_stats['folders']
            file_count += sub_stats['files']
        
        return {'folders': folder_count, 'files': file_count}
    
    # Search for files containing a pattern
    def search_files(self, pattern):
        results = []
        
        # Search in current folder
        for file in self.files:
            if pattern.lower() in file.lower():
                results.append({
                    'file': file,
                    'path': self.get_path(),
                    'full_path': f"{self.get_path()}/{file}"
                })
        
        # Search in subfolders
        for subfolder in self.subfolders:
            results.extend(subfolder.search_files(pattern))
        
        return results

# File System Manager Class
class FileSystemTree:
    def __init__(self):
        self.root = Folder("Root")
    
    def create_folder_path(self, path):
        """Create nested folders from a path like 'Documents/Projects/Python'"""
        folders = path.split('/')
        current = self.root
        
        for folder_name in folders:
            existing = None
            for subfolder in current.subfolders:
                if subfolder.name == folder_name:
                    existing = subfolder
                    break
            
            if existing:
                current = existing
            else:
                current = current.add_subfolder(folder_name)
        
        return current
    
    def navigate_to_folder(self, path):
        """Navigate to a folder using path"""
        if path == "" or path == "/":
            return self.root
        
        folders = path.split('/')
        current = self.root
        
        for folder_name in folders:
            if folder_name:  # Skip empty strings
                found = False
                for subfolder in current.subfolders:
                    if subfolder.name == folder_name:
                        current = subfolder
                        found = True
                        break
                if not found:
                    return None
        
        return current

# Demo usage
if __name__ == "__main__":
    # Create file system
    fs = FileSystemTree()
    
    # Create folder structure
    documents = fs.create_folder_path("Documents")
    pictures = fs.create_folder_path("Pictures")
    music = fs.create_folder_path("Music")
    
    assignments = fs.create_folder_path("Documents/Assignments")
    notes = fs.create_folder_path("Documents/Notes")
    vacations = fs.create_folder_path("Pictures/Vacations")
    rock = fs.create_folder_path("Music/Rock")
    jazz = fs.create_folder_path("Music/Jazz")
    classic = fs.create_folder_path("Music/Classic")
    
    # Add some files
    assignments.add_file("DSA_Project.pdf")
    assignments.add_file("Math_Assignment.docx")
    notes.add_file("Lecture_Notes.txt")
    rock.add_file("song1.mp3")
    rock.add_file("song2.mp3")
    vacations.add_file("beach.jpg")
    vacations.add_file("mountain.png")
    
    print("=== FOLDER HIERARCHY ===")
    fs.root.print_hierarchy()
    
    print("\n=== PREORDER TRAVERSAL ===")
    fs.root.preorder_traversal()
    
    print("\n=== POSTORDER TRAVERSAL ===")
    fs.root.postorder_traversal()
    
    print("\n=== LEVEL ORDER TRAVERSAL ===")
    fs.root.level_order_traversal()
    
    print("\n=== STATISTICS ===")
    stats = fs.root.get_statistics()
    print(f"Total Folders: {stats['folders']}")
    print(f"Total Files: {stats['files']}")
    
    print("\n=== SEARCH FILES (containing 'song') ===")
    results = fs.root.search_files("song")
    for result in results:
        print(f"Found: {result['file']} in {result['path']}")
    
    # Navigate to specific folder
    music_folder = fs.navigate_to_folder("Music")
    if music_folder:
        print(f"\n=== MUSIC FOLDER CONTENTS ===")
        music_folder.print_hierarchy()
