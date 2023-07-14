"""Module containing all the hardcoded variables"""


class ConfigErrorMessages:
    """Configuration of displayed error messages"""
    ERROR_MSG_IMPORT_PATH = "Chosen Path for import does not exist."
    ERROR_MSG_FILE_FORMAT_IMPORT_JSON = "The file format format does not match the schema. The json file needs a key 'label' and a key 'functional_expression' with the information."
    ERROR_MSG_FUNCTION_LABEL_INVALID = """The added label is invalid.
        Labels have to start with a letter and can only contain the following characters:
        {[a-zA-Z0-9_]}"""
    ERROR_MSG_NO_ALTERNATIVE_SELECTED = "To use this function an alternative needs to be selected."
    ERROR_MSG_NO_DERIVATIVE_SELECTED = "To use this function a derivative needs to be selected."
    ERROR_MSG_CANT_SELECT_RAW_DATA = "Non derived data can not be edited."


class ConfigExpressionErrors:
    """Configuration of errors associated with FunctionalExpressions"""
    COLOR_HEX = 0x0


class ConfigRegexPatterns:
    """Configuration of used regex patterns"""
    PATTERN_FUNCTION_LABEL = "^[a-zA-Z]+[a-zA-Z0-9_]*$"


class ConfigFiles:
    """Configuration of path strings"""
    PATH_JSON_FILE = "%s/%s.json"
    SEPARATOR_CSV = ";"


class ConfigModelWidget:
    """Configurations of the Model Widget"""
    INDEX_LABEL = 0
    INDEX_DEFINITION = 1
    INDEX_AVAILABILITY = 2
    HEADERS = ['Label', 'Definition', 'Availability Condition']


class ConfigColumnWidget:
    """Configuration of the Column Widget"""
    INDEX_LABEL = 0
    INDEX_TYPE = 1
    INDEX_DEFINITION = 2
    HEADERS = ['Label', 'Type', 'Definition']


class ConfigFileMenu:
    """ Configuration of the FileMenu"""
    OPEN_PROJECT_DIALOG_TITLE = 'Open Project'
    SAVE_PROJECT_DIALOG_TITLE = 'Save Project'
    SAVE_PROJECT_AS_DIALOG_TITLE = 'Save Project As'
    IMPORT_DATA_DIALOG_TITLE = 'Import Data'
    EXPORT_DATA_DIALOG_TITLE = 'Export To'
    DIRECTORY_FILE_FORMAT = 'Directory (*.dir)'
    CSV_FILE_FORMAT = 'CSV File (*.csv)'
