from PyQt5.QtWidgets import QFileDialog


class FileManagementWindow(QFileDialog):
    """
    This represents the FileManagementWindow, which is a
    file dialog for the user to choose a path or file
    """
    def __init__(self):
        super().__init__()

    def open_file(self, title: str, file_mode: QFileDialog.FileMode, file_format: str):
        """
        This opens a file dialog for opening files and paths
        @param title: the dialog's title
        @type title: str
        @param file_mode: determines which files can be selected
        @type file_mode: QFileDialog.FileMode
        @param file_format: determines which files to be shown (besides directories)
        @type file_format: str
        @return: the path
        @rtype: str
        """
        self.setOption(QFileDialog.DontUseNativeDialog)
        self.setWindowTitle(title)
        self.setFileMode(file_mode)
        self.setNameFilter(file_format)
        if self.exec_():
            return self.selectedFiles()[0]

    def save_file(self, title: str, file_format: str):
        """
        This opens a file dialog for saving and exporting files
        @param title: the dialog's title
        @type title: str
        @param file_format: the files to be shown (besides directories)
        @type file_format: str
        @return: the path
        @rtype: str
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        result = self.getSaveFileName(self, title, '',
                                      file_format, options=options)
        if result:
            return result[0]
