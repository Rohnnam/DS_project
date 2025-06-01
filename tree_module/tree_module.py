import java.util.ArrayList;
import java.util.List;

// Folder node class
class Folder {
    String name;
    List<Folder> subfolders;

    public Folder(String name) {
        this.name = name;
        this.subfolders = new ArrayList<>();
    }

    // Method to add a subfolder
    public void addSubfolder(Folder folder) {
        subfolders.add(folder);
    }

    // Method to print the folder hierarchy
    public void printHierarchy(String indent) {
        System.out.println(indent + "📁 " + name);
        for (Folder sub : subfolders) {
            sub.printHierarchy(indent + "    ");
        }
    }
}

// Main class
public class FolderHierarchyTree {
    public static void main(String[] args) {
        // Create folders
        Folder root = new Folder("Root");
        
        Folder documents = new Folder("Documents");
        Folder pictures = new Folder("Pictures");
        Folder music = new Folder("Music");

        Folder assignments = new Folder("Assignments");
        Folder notes = new Folder("Notes");

        Folder vacations = new Folder("Vacations");

        Folder rock = new Folder("Rock");
        Folder jazz = new Folder("Jazz");

        // Build the tree structure
        root.addSubfolder(documents);
        root.addSubfolder(pictures);
        root.addSubfolder(music);

        documents.addSubfolder(assignments);
        documents.addSubfolder(notes);

        pictures.addSubfolder(vacations);

        music.addSubfolder(rock);
        music.addSubfolder(jazz);

        // Print the hierarchy
        System.out.println("Folder Hierarchy:");
        root.printHierarchy("");
    }
}

