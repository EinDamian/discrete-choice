from __future__ import annotations
import json
import pandas as pd
import numpy as np

from src.config import ConfigFiles


class FileManager:
    """Interface that takes care of reading in files and making files for the export."""

    @staticmethod
    def export(path: str, file_content: object = None) -> bool:
        """Method responsible for the export of general files.
        Currently implemented for JSON files.

        Args:
            path (str): The path where the file should be added, containing the filename.
            file_content (object): The content to be written in the file.

        Returns:
            bool: True if export was successful. Else an error is raised.
        """
        try:
            if path.endswith("json"):
                FileManager.__write_string_file(path, file_content)
            elif path.endswith("csv"):
                FileManager.__write_csv_file(path, file_content)
            return True

        except OSError as error:
            return error

    @staticmethod
    def import_(path: str) -> object:
        print(f'import {path}')

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
                    return json.loads(file.read())
            except OSError as error:
                return error
        elif path.endswith('.csv'):
            return FileManager.__read_csv_file(path)

    @staticmethod
    def __write_string_file(full_path: str, file_content: str):
        """Writes a string into a json file.

        Args:
            full_path (str): full path to file.
            file_content (str): the json string. 
        """
        with open(full_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

    @staticmethod
    def __write_csv_file(full_path: str, file_content: pd.DataFrame):
        """Export a pandas Dataframe into a csv file.

        Args:
            full_path (str): full path to file.
            file_content (pd.DataFrame): the pandas Dataframe containing the data to be exported.
        """
        file_content.to_csv(full_path, sep=ConfigFiles.DEFAULT_SEPARATOR_CSV)
    
    
    @staticmethod
    def __read_csv_file(path: str) -> pd.DataFrame:
        """Reads csv files into a pandas Dataframe. 
        To find the correct decimal points and cell separators the options are counted and the most popular one is chosen.

        Args:
            path (str): Path to the chosen file.

        Returns:
            pd.DataFrame: The pandas dataframe containing the data from the csv file.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                temp_string = file.read()
        except OSError as error:
            return error
        
        separator_counts = []
        for sep in ConfigFiles.POSSIBLE_SEPARATORS:
             separator_counts.append(temp_string.count(sep))
        
        decimal_counts = []
        for dec in ConfigFiles.POSSIBLE_DECIMAL_POINTS:
             decimal_counts.append(temp_string.count(dec))
                
        separator = ConfigFiles.POSSIBLE_SEPARATORS[separator_counts.index(max(separator_counts))]
        decimal_point = ConfigFiles.POSSIBLE_DECIMAL_POINTS[decimal_counts.index(max(decimal_counts))]
        return pd.read_csv(path, sep=separator, decimal=decimal_point)