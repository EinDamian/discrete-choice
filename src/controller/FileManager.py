from __future__ import annotations
import json

class FileManager:
    """Interface that takes care of reading in files and making files for the export."""

    def export(self, path: str) -> bool:
        """Blueprint for the export of files.

        Args:
            path (str): Path to where the files will be saved.

        Raises:
            NotImplementedError: This is an abstract function and is not implemented.

        Returns:
            bool: True id export was successful, else False.
        """
        raise NotImplementedError

    def import_(self, path: str) -> object:
        """Function that deals with reading the files to be imported from the specified path. 
        Currently supports: JSON

        Args:
            path (str): Path to the file to be imported.

        Returns:
            object: The content of the file.
        """
        if path.endswith('.json'):
            try:
                with open(path, "r", encoding="utf-8") as file:
                    return json.loads(file)
            except OSError as error:
                return error
        
        
