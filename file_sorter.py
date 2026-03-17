import os
import shutil
from datetime import datetime
from mutagen import File

# Constants for directory names
MEDIA_DIR = 'media'
DATE_FORMAT = '%Y-%m-%d'

def extract_metadata(file_path):
    """Extract metadata using mutagen library"""
    try:
        audio_file = File(file_path)
        if audio_file is not None:
            # Try to get creation date from various metadata fields
            creation_date = None
            if hasattr(audio_file, 'tags') and audio_file.tags:
                # Try common date fields
                for key in ['TDRC', 'date', 'DATE', 'creation_time']:
                    if key in audio_file.tags:
                        creation_date = str(audio_file.tags[key][0])
                        break
            return {'creation_date': creation_date}
        return {}
    except Exception:
        return {}

def sort_files_by_date(source_dir):
    """
    Sort media files in the source directory into folders by date.
    Files are moved into folders named by the extraction date of the media.
    """
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Create media directory if it doesn't exist
    media_path = os.path.join(source_dir, MEDIA_DIR)
    os.makedirs(media_path, exist_ok=True)

    for filename in os.listdir(source_dir):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov', '.jpg', '.png')):
            file_path = os.path.join(source_dir, filename)
            try:
                # Extract metadata and get the creation date
                metadata = extract_metadata(file_path)
                creation_date = metadata.get('creation_date')
                
                # Fallback to last modified date if creation date is not available
                if not creation_date:
                    creation_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(DATE_FORMAT)
                else:
                    # Handle case where creation_date might be a datetime object or string
                    if isinstance(creation_date, datetime):
                        creation_date = creation_date.strftime(DATE_FORMAT)
                    else:
                        # Try to parse the string as a date
                        try:
                            parsed_date = datetime.fromisoformat(str(creation_date).replace('Z', '+00:00'))
                            creation_date = parsed_date.strftime(DATE_FORMAT)
                        except (ValueError, TypeError):
                            # If parsing fails, use file modification time
                            creation_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(DATE_FORMAT)

                # Create a directory for the date if it doesn't exist
                date_dir = os.path.join(media_path, creation_date)
                os.makedirs(date_dir, exist_ok=True)

                # Move the file to the corresponding date directory
                shutil.move(file_path, os.path.join(date_dir, filename))
                print(f"Moved '{filename}' to '{date_dir}'")

            except Exception as e:
                print(f"Error processing '{filename}': {e}")

def sort_files_by_type(source_dir):
    """
    Sort media files in the source directory into folders by file type.
    Files are moved into folders named after their file extensions.
    """
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Create media directory if it doesn't exist
    media_path = os.path.join(source_dir, MEDIA_DIR)
    os.makedirs(media_path, exist_ok=True)

    for filename in os.listdir(source_dir):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov', '.jpg', '.png')):
            file_path = os.path.join(source_dir, filename)
            file_extension = filename.split('.')[-1].lower()
            type_dir = os.path.join(media_path, file_extension)

            try:
                # Create directory for the file type if it doesn't exist
                os.makedirs(type_dir, exist_ok=True)

                # Move the file to the corresponding type directory
                shutil.move(file_path, os.path.join(type_dir, filename))
                print(f"Moved '{filename}' to '{type_dir}'")

            except Exception as e:
                print(f"Error processing '{filename}': {e}")

# TODO: Add a function to sort by both date and type for more organization
# TODO: Consider adding a command-line interface to allow user input for sorting method

if __name__ == '__main__':
    # Example usage
    source_directory = 'path/to/your/kdenlive/project'  # Change this to your project path
    sort_files_by_date(source_directory)
    # Or sort_files_by_type(source_directory) for type-based sorting
