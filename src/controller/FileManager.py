from __future__ import annotations
import json

class FileManager:
    """Interface that takes care of reading in files and making files for the export."""

    def export(self, path: str, file_content: str = "", file_type: str = "json", filename: str|None = None) -> bool:
        """Method responsible for the export of files.

        Args:
            path (str): The path where the file should be added (with the filename already?).
            file_content (str): The text to be written in the file.
            file_type (str): The type of file/ the file extension.

        Returns:
            bool: True if export was successful. Else an error is raised.
        """
        try:
            if filename is not None:
                with open(path + "/" + filename + "." + file_type, 'w', encoding="utf-8") as file:
                    file.write(file_content)
                return True
            
            with open(path + "." + file_type, 'w', encoding="utf-8") as file:
                file.write(file_content)
            return True
        except OSError as error:
            return error


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
        
        
