class Folder:
    def __init__(self, name):
        self.name = name
        self.subfolders = []

    # Add a subfolder
    def add_subfolder(self, folder):
        self.subfolders.append(folder)

    # Print the folder hierarchy
    def print_hierarchy(self, indent=""):
        print(f"{indent}📁 {self.name}")
        for sub in self.subfolders:
            sub.print_hierarchy(indent + "    ")

# Build the folder structure
if __name__ == "__main__":
    # Create folders
    root = Folder("Root")

    documents = Folder("Documents")
    pictures = Folder("Pictures")
    music = Folder("Music")

    assignments = Folder("Assignments")
    notes = Folder("Notes")

    vacations = Folder("Vacations")

    rock = Folder("Rock")
    jazz = Folder("Jazz")

    # Build the hierarchy
    root.add_subfolder(documents)
    root.add_subfolder(pictures)
    root.add_subfolder(music)

    documents.add_subfolder(assignments)
    documents.add_subfolder(notes)

    pictures.add_subfolder(vacations)

    music.add_subfolder(rock)
    music.add_subf_


