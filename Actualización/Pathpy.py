from typing import Optional
import os

def Get_Most_Recent_Backup(Directory: str) -> Optional[str]:

    """
    Gets the most recent file in a directory based on modification time.

    Args:
        Directory (str): The path to the directory.

    Returns:
        Optional[str]: The path to the most recent file or None if no files are found.

    """

    # List all files in the directory.
    Files = [os.path.join(Directory, File) for File in os.listdir(Directory) if os.path.isfile(os.path.join(Directory, File))]
    
    # Check if the directory is empty.
    if not Files:
        return None
    
    # Get the most recent file by modification time.
    Most_Recent_Backup = max(Files, key=os.path.getmtime)
    
    return Most_Recent_Backup