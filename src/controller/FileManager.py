from __future__ import annotations
import json
import pandas as pd

class FileManager:
    """Interface that takes care of reading in files and making files for the export."""

    def export(self, path: str, file_content: object = None) -> bool:
        """Method responsible for the export of general files.
        Currently implemented for JSON files.

        Args:
            path (str): The path where the file should be added, containing the filename.
            file_content (str): The text to be written in the file.
            file_type (str): The type of file/ the file extension.

        Returns:
            bool: True if export was successful. Else an error is raised.
        """       
        try:
            if path.endswith("json"):
                self.__write_string_file(path, file_content)
            elif path.endswith("csv"):
                self.__write_csv_file(path, file_content)
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
        elif path.endswith('.csv'):
            return pd.read_csv(path)
                
        
    def __write_string_file(self, full_path: str, file_content: str):
        """Writes a string into a json file.

        Args:
            full_path (str): full path to file.
            file_content (str): the json string. 
        """
        with open(full_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

    
    def __write_csv_file(self, full_path: str, file_content: pd.DataFrame):
        """Export a pandas Dataframe into a csv file.

        Args:
            full_path (str): full path to file.
            file_content (pd.DataFrame): the pandas Dataframe containing the data to be exported.
        """
        file_content.to_csv(full_path)
        