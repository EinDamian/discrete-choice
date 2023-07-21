from PyQt5.QtWidgets import QFileDialog

from src.config import ConfigFileManagementWindow as Cfg


class FileManagementWindow(QFileDialog):
    """
    This represents the FileManagementWindow, which is a
    file dialog for the user to choose a path or file
    """

    def __init__(self):
        super().__init__()

    def open_file(self, title: str, file_mode: QFileDialog.FileMode, file_format: str | None) -> str:
        """
        This opens a file dialog for opening files and paths
        @param title: the dialog's title
        @type title: str
        @param file_mode: determines which files can be selected
        @type file_mode: QFileDialog.FileMode
        @param file_format: determines which files to be shown (besides directories).
        Use None if no filter is needed
        @type file_format: str or None
        @return: the path
        @rtype: str
        """
        self.setWindowTitle(title)
        self.setFileMode(file_mode)
        if file_format is not None:
            self.setNameFilter(file_format)
        if self.exec_():
            return self.selectedFiles()[0]

    def save_file(self, title: str, file_format: str) -> str | None:
        """
        This opens a file dialog for saving and exporting files
        @param title: the dialog's title
        @type title: str
        @param file_format: the files to be shown (besides directories)
        @type file_format: str
        @return: the path
        @rtype: str
        """
        result = self.getSaveFileName(self, title, '', file_format)
        # In some operating systems, the native dialog seems to add the file extension directly to the project's name
        if result:
            path = result[0]
            if path[Cfg.LAST_FOURTH_POSITION:] == Cfg.DIR_FILE_EXTENSIONS:
                path = path[:len(path) - len(Cfg.DIR_FILE_EXTENSIONS)]
            return path

    def choose_files(self, title: str, file_mode: QFileDialog.FileMode = QFileDialog.AnyFile, name_filter: str = "") -> \
            list[str]:
        """ This method opens a file dialog to choose multiple files.

        Args:
            title (str): title of the file dialog.
            file_mode (QFileDialog.FileMode, optional): The File mode that determines what files can be chosen. Defaults to QFileDialog.AnyFile.
            name_filter (str, optional): A name filter to limit what files can be chosen. Defaults to "" and then allows all files.

        Returns:
            list[str]: List of the chosen paths.
        """
        self.setFileMode(file_mode)
        self.setWindowTitle(title)
        self.setNameFilter(name_filter)
        self.setViewMode(QFileDialog.Detail)
        if self.exec_():
            return self.selectedFiles()
