import os
import json
import shutil
from datetime import datetime

# Main script to organize Kdenlive project files
class KdenliveProjectOrganizer:
    def __init__(self, project_file, media_folder):
        self.project_file = project_file
        self.media_folder = media_folder
        self.metadata = {}

    def load_project(self):
        """Load Kdenlive project file to extract metadata."""
        try:
            with open(self.project_file, 'r') as file:
                self.metadata = json.load(file)
                print(f"Loaded project metadata from {self.project_file}")
        except FileNotFoundError:
            print(f"Error: Project file {self.project_file} not found.")
            return False
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the project file.")
            return False
        return True

    def organize_media(self):
        """Organize media files based on extracted metadata."""
        if not self.metadata:
            print("No metadata to organize media. Please load a project file first.")
            return

        try:
            media_files = self.metadata.get('media', [])
            for media in media_files:
                file_path = os.path.join(self.media_folder, media['file'])
                if os.path.exists(file_path):
                    date_str = media.get('date', datetime.now().strftime('%Y-%m-%d'))
                    media_type = media.get('type', 'unknown')
                    target_folder = os.path.join(self.media_folder, date_str, media_type)

                    os.makedirs(target_folder, exist_ok=True)  # Create folder if it doesn't exist
                    shutil.copy(file_path, target_folder)  # Copy file to the new folder
                    print(f"Copied {file_path} to {target_folder}")
                else:
                    print(f"Warning: Media file {file_path} does not exist.")
        except Exception as e:
            print(f"Error while organizing media: {e}")

def main():
    project_file = 'path/to/your/project.kdenlive'  # TODO: Update with actual project path
    media_folder = 'path/to/your/media'  # TODO: Update with actual media folder path

    organizer = KdenliveProjectOrganizer(project_file, media_folder)

    if organizer.load_project():
        organizer.organize_media()

if __name__ == "__main__":
    main()

# TODO: Add command-line argument support for dynamic file paths.
# TODO: Implement logging instead of print for production use.
# TODO: Enhance error handling for various edge cases (e.g., permission issues).
# TODO: Consider adding a feature to delete duplicates.
