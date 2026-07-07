"""
This utility copies all the contents from a source directory to a destination directory recursively,
before that it empties the destination directory.
"""
from pathlib import Path
import shutil

# Using Path.home() / ... to properly resolve the "~" home directory shortcut
SOURCE = Path.home() / "workspace/boot-dev/static-site-generator/static"
DESTINATION = Path.home() / "workspace/boot-dev/static-site-generator/public"

def transfer_contents():
    # 1. Validation Checks
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source path '{SOURCE}' doesn't exist.")
    
    # 2. Empty the Destination Directory
    if DESTINATION.exists():
        print(f"Clearing destination directory: {DESTINATION}")
        # Delete the destination directory and all its contents recursively
        shutil.rmtree(DESTINATION)
    
    # Recreate the empty destination directory
    DESTINATION.mkdir(parents=True, exist_ok=True)
    
    # 3. Copy contents recursively
    print(f"Copying contents from {SOURCE} to {DESTINATION}...")
    
    # Iterate through everything directly inside the source directory
    for item in SOURCE.iterdir():
        dest_item = DESTINATION / item.name
        if item.is_dir():
            # shutil.copytree copies a directory and everything inside it recursively
            shutil.copytree(item, dest_item)
        else:
            # shutil.copy2 copies a file along with its metadata (permissions, times)
            shutil.copy2(item, dest_item)

    print("Transfer complete!")

if __name__ == "__main__":
    transfer_contents()