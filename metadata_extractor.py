import os
import json
import logging
from datetime import datetime
from mutagen import File as MutagenFile
from mutagen.id3 import ID3NoHeaderError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MetadataExtractor:
    def __init__(self, media_folder):
        self.media_folder = media_folder
        self.metadata = []

    def extract_metadata(self):
        """Extract metadata from all media files in the specified folder."""
        if not os.path.exists(self.media_folder):
            logging.error(f"Folder {self.media_folder} does not exist.")
            return
        
        for root, dirs, files in os.walk(self.media_folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    self._extract_from_file(file_path)
                except Exception as e:
                    logging.warning(f"Could not extract metadata from {file_path}: {e}")

    def _extract_from_file(self, file_path):
        """Extract metadata from a single file."""
        logging.info(f"Extracting metadata from {file_path}")
        
        # Use Mutagen to read file metadata
        media = MutagenFile(file_path)
        
        if media is None:
            logging.warning(f"No metadata found for {file_path}")
            return
        
        try:
            # Safely get file type
            file_type = 'unknown'
            if hasattr(media, 'mime') and media.mime and len(media.mime) > 0:
                file_type = media.mime[0]
            
            # Safely get duration
            duration = None
            if hasattr(media, 'info') and media.info and hasattr(media.info, 'length'):
                duration = media.info.length
            
            metadata = {
                'file_name': os.path.basename(file_path),
                'file_path': file_path,
                'file_type': file_type,
                'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)),
                'duration': duration,
                'tags': self._get_tags(media)
            }
            self.metadata.append(metadata)
            logging.info(f"Metadata extracted: {metadata}")
        except Exception as e:
            logging.error(f"Error reading metadata for {file_path}: {e}")

    def _get_tags(self, media):
        """Retrieve tags from the media file."""
        tags = {}
        if hasattr(media, 'tags') and media.tags:
            for key in media.tags:
                tags[key] = media.tags[key]
        return tags

    def save_metadata(self, output_file):
        """Save the extracted metadata to a JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.metadata, f, indent=4, default=str)
            logging.info(f"Metadata saved to {output_file}")
        except Exception as e:
            logging.error(f"Failed to save metadata to {output_file}: {e}")

# Example usage, this would be in the main application
if __name__ == "__main__":
    media_folder = './media'  # Path to your media folder
    output_file = 'metadata.json'

    extractor = MetadataExtractor(media_folder)
    extractor.extract_metadata()
    extractor.save_metadata(output_file)

# TODO: Add support for more media types
# TODO: Improve error handling for specific media formats
# TODO: Add command-line arguments for flexibility
# TODO: Consider using a database for metadata storage instead of JSON
