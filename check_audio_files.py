import os
import sys
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AudioFileTester")

def check_audio_files(file_list_path, hop_length=256):
    """
    Check audio files in the list and report which ones are valid/invalid
    """
    if not os.path.exists(file_list_path):
        logger.error(f"File list not found: {file_list_path}")
        return
    
    # Read the file list
    with open(file_list_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    audiopaths_sid_text = []
    for line in lines:
        try:
            path_and_rest = line.strip().split("|")
            _id = path_and_rest[0]
            # Store the first item (file path) and the rest as context
            audiopaths_sid_text.append([_id] + path_and_rest[1:])
        except Exception as e:
            logger.error(f"Error parsing line: {line}, error: {e}")
    
    logger.info(f"Found {len(audiopaths_sid_text)} entries in the file list")
    
    # Check each file
    valid_files = []
    invalid_files = []
    skipped = 0
    
    for item in tqdm(audiopaths_sid_text):
        try:
            _id = item[0]
            # Convert path separators to OS-specific format
            audiopath = os.path.normpath(_id)
            
            if not os.path.exists(audiopath):
                # Log path details for debugging
                logger.warning(f"Audio file not found at direct path: {audiopath}")
                logger.warning(f"Current working directory: {os.getcwd()}")
                
                # Try different path variations including melo/ prefix
                possible_paths = [
                    audiopath,
                    os.path.join(os.getcwd(), audiopath),
                    os.path.normpath(os.path.join(os.getcwd(), _id)),
                    os.path.normpath(os.path.join(os.getcwd(), _id.replace('/', '\\'))),
                    # Add melo/ prefix if the path starts with data/
                    os.path.normpath('melo/' + _id) if _id.startswith('data/') else None,
                    os.path.join(os.getcwd(), 'melo', _id)
                ]
                
                # Filter out None values
                possible_paths = [p for p in possible_paths if p]
                
                found = False
                for path in possible_paths:
                    if os.path.exists(path):
                        audiopath = path
                        found = True
                        logger.info(f"Found file at alternate path: {path}")
                        break
                
                if not found:
                    logger.warning(f"Audio file not found at any path: {_id}")
                    logger.warning(f"Tried paths: {possible_paths}")
                    invalid_files.append((_id, "File not found"))
                    skipped += 1
                    continue
            
            # Check file size to make sure it's a valid audio file
            try:
                file_size = os.path.getsize(audiopath)
                if file_size <= 0:
                    logger.warning(f"File has zero size: {audiopath}")
                    invalid_files.append((audiopath, "Zero file size"))
                    skipped += 1
                    continue
                
                valid_files.append(audiopath)
            except Exception as e:
                logger.error(f"Error getting file size for {audiopath}: {e}")
                invalid_files.append((audiopath, f"Error: {str(e)}"))
                skipped += 1
        except Exception as e:
            logger.error(f"Error processing item {item}: {e}")
            invalid_files.append((str(item), f"Processing error: {str(e)}"))
            skipped += 1
    
    logger.info(f"Valid files: {len(valid_files)}, Invalid files: {len(invalid_files)}, Skipped: {skipped}")
    
    # Print details of invalid files
    if invalid_files:
        logger.warning("Invalid files:")
        for file_path, reason in invalid_files:
            logger.warning(f"  {file_path}: {reason}")
    
    # Print details of valid files
    if valid_files:
        logger.info("Valid files:")
        for file_path in valid_files:
            logger.info(f"  {file_path}")
    
    return valid_files, invalid_files

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_list_path = sys.argv[1]
    else:
        file_list_path = "melo/data/example/val.list"
    
    logger.info(f"Checking audio files in {file_list_path}")
    valid_files, invalid_files = check_audio_files(file_list_path)
    
    print(f"\nSummary:")
    print(f"- Valid files: {len(valid_files)}")
    print(f"- Invalid files: {len(invalid_files)}")
    
    if not valid_files:
        print("\nNo valid audio files found. This matches the error in TextAudioSpeakerLoader._filter()") 