import unittest
from unittest.mock import mock_open, patch, MagicMock
import pandas as pd
from src.controller.FileManager import FileManager
from src.config import ConfigFiles


class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.file_manager = FileManager()

    def test_export_json_positive(self):
        with patch('builtins.open', create=True) as mock_open:
            mock_file = MagicMock()
            mock_open.return_value = mock_file
            result = self.file_manager.export("path/to/export.json", {"key": "value"})
            self.assertTrue(result)
            mock_open.assert_called_once_with("path/to/export.json", 'w', encoding="utf-8")

    def test_export_csv_positive(self):
        pd_mock = MagicMock()
        df_mock = MagicMock()
        pd_mock.DataFrame.return_value = df_mock
        with patch.dict('sys.modules', pandas=pd_mock):
            result = self.file_manager.export("path/to/export.csv", df_mock)
            self.assertTrue(result)
            df_mock.to_csv.assert_called_once_with("path/to/export.csv", sep=ConfigFiles.DEFAULT_SEPARATOR_CSV)

    def test_export_json_negative(self):
        with patch('builtins.open', create=True) as mock_open:
            mock_open.side_effect = OSError("Error writing file")
            result = self.file_manager.export("path/to/export.json", {"key": "value"})
            self.assertIsInstance(result, OSError)

    def test_import_json_positive(self):
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            result = self.file_manager.import_("test.json")
            self.assertEqual(result, {"key": "value"})

    def test_import_csv_positive(self):
        with patch("builtins.open", mock_open(read_data='A,B\n1,4\n2,5\n3,6\n')):
            result = self.file_manager.import_("test.csv")
            expected_dataframe = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
            pd.testing.assert_frame_equal(result, expected_dataframe)

    def test_import_json_negative(self):
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = OSError("Test Error")
            result = self.file_manager.import_("test.json")
            self.assertIsInstance(result, OSError)

    def test_import_csv_negative(self):
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = OSError("Test Error")
            result = self.file_manager.import_("test.csv")
            self.assertIsInstance(result, OSError)

    def test_read_csv_file_positive(self):
        csv_content = 'A,B\n1,4\n2,5\n3,6\n'
        with patch("builtins.open", mock_open(read_data=csv_content)):
            result = self.file_manager._FileManager__read_csv_file("test.csv")
            expected_dataframe = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
            pd.testing.assert_frame_equal(result, expected_dataframe)

    def test_read_csv_file_negative(self):
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = OSError("Test Error")
            result = self.file_manager._FileManager__read_csv_file("test.csv")
            self.assertIsInstance(result, OSError)


if __name__ == '__main__':
    unittest.main()
