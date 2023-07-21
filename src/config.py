"""Module containing all the hardcoded variables"""


class ConfigErrorMessages:
    """Configuration of displayed error messages"""
    ERROR_MSG_IMPORT_PATH = "Chosen Path for import does not exist."
    ERROR_MSG_FILE_FORMAT_IMPORT_JSON = "The file format format does not match the schema. The json file needs a key 'label' and a key 'functional_expression' with the correct information."
    ERROR_MSG_MISSING_KEY = "\nThe key %s is missing from the imported file.\nFile could not be imported"
    ERROR_MSG_FUNCTION_LABEL_INVALID = """The added label is invalid.
        Labels have to start with a letter and can only contain the following characters:
        {[a-zA-Z0-9_]}"""
    ERROR_MSG_NO_ALTERNATIVE_SELECTED = "To use this function an alternative needs to be selected."
    ERROR_MSG_NO_DERIVATIVE_SELECTED = "To use this function a derivative needs to be selected."
    ERROR_MSG_CANT_SELECT_RAW_DATA = "Non derived data can not be edited."
    ERROR_MSG_FUNCTION_NOT_EXISTENT = "The selected derivative or alternative does not exist."
    ERROR_MSG_CHOICE_INDEX_NOT_INTEGER = "The choice index needs to be an integer."


class ConfigExpressionErrors:
    """Configuration of errors associated with FunctionalExpressions"""
    COLOR_HEX = 0xFF3030

    ERROR_INVALID_SYNTAX = "Invalid syntax."
    ERROR_ILLEGAL_FUNCTION = "Function should not be called."
    ERROR_BRACKET_NOT_CLOSED = "Bracket was never closed."
    ERROR_UNMATCHED_BRACKET = "Bracket was never opened."

    ERROR_VARIABLE_NON_EXISTENT = "Variable name '{0}' does not exist."
    ERROR_CYCLIC_DEPENDENCY = "Variable leads to cyclic dependency: {0}."
    ERROR_INVALID_VARIABLE = "Variable '{0}' is not valid."


class ConfigRegexPatterns:
    """Configuration of used regex patterns"""
    PATTERN_FUNCTION_LABEL = "^[a-zA-Z]+[a-zA-Z0-9_]*$"
    PATTERN_DATATYPES = "[a-zA-Z]+"


class ConfigFiles:
    """Configuration of path strings"""
    PATH_JSON_FILE = "%s/%s.json"
    DEFAULT_SEPARATOR_CSV = ";"
    POSSIBLE_SEPARATORS = [";", ",", "\t"]
    DEFAULT_DECIMAL_POINT = ","
    POSSIBLE_DECIMAL_POINTS = [",", "."]


class ConfigModelWidget:
    """Configuration of the Model Widget"""
    INDEX_LABEL = 0
    INDEX_DEFINITION = 1
    INDEX_AVAILABILITY = 2
    INDEX_CHOICE = 3
    HEADERS = ['Label', 'Definition', 'Availability Condition', 'Choice Index']
    BUTTON_NAME_ADDITION = "Add"
    WINDOW_TITLE_ADDITION = "Add new Alternative:"
    FILE_TYPE_FILTER_ALTERNATIVE_IMPORT = "Text files (*.json)"
    ALTERNATIVE_IMPORT_WINDOW_TITLE = "Select Alternative Files for Import:"
    ALTERNATIVE_EXPORT_WINDOW_TITLE = "Choose a path to export Alternative to:"


class ConfigColumnWidget:
    """Configuration of the Column Widget"""
    INDEX_LABEL = 0
    INDEX_TYPE = 1
    INDEX_DEFINITION = 2
    HEADERS = ['Label', 'Type', 'Definition']
    BUTTON_NAME_ADDITION = "Add"
    WINDOW_TITLE_ADDITION = "Add new Derivative:"
    FILLER_EMPTY_DEFINITION = "-"
    FILLER_UNDETERMINED_DATATYPE = "?"
    FILE_TYPE_FILTER_DERIVATIVE_IMPORT = "Text files (*.json)"
    DERIVATIVE_IMPORT_WINDOW_TITLE = "Select Derivative Files for Import:"
    DERIVATIVE_EXPORT_WINDOW_TITLE = "Choose a path to export derivative:"


class ConfigFunctionHighlighting:
    """Configurations of the Highlighting of Functions with errors"""
    OPACITY = 128
    MISTAKE_TOOLTIP_START = "Found Mistakes:\n"
    LIST_CHARACTER_MISTAKES_TOOLTIP = "\n\u2022"
    HIGHLIGHTING_OFFSET = 5


class ConfigFileManagementWindow:
    DIR_FILE_EXTENSIONS = '.dir'
    LAST_FOURTH_POSITION = -4


class ConfigFileMenu:
    """ Configuration of the FileMenu"""
    OPEN_PROJECT_DIALOG_TITLE = 'Open Project'
    SAVE_PROJECT_DIALOG_TITLE = 'Save Project'
    SAVE_PROJECT_AS_DIALOG_TITLE = 'Save Project As'
    IMPORT_DATA_DIALOG_TITLE = 'Import Data'
    EXPORT_DATA_DIALOG_TITLE = 'Export To'
    DIRECTORY_FILE_FORMAT = 'Directory (*)'
    CSV_FILE_FORMAT = 'CSV File (*.csv)'
    WARNING_DIALOG_TITLE = 'Warning!'
    MESSAGE_DIALOG_SAVE_BEFORE_NEW = 'Do you wish to save the project before opening a new one?'
    MESSAGE_DIALOG_SAVE_BEFORE_OTHER = 'Do you wish to save the project before opening another one?'


class ConfigEvaluationWidget:
    EXPORT_DIALOG_TITLE = 'Export File'
    DIRECTORY_FILE_FORMAT = 'Directory (*.dir)'


class ConfigThresholdWindow:
    FIELD_MIN_WIDTH = 200
    FIELD_MIN_HEIGHT = 0
    NUM_OF_STRETCH = 1
    DEFAULT_THRESHOLD = 0


class ConfigThresholdField:
    MAX_THRESHOLD_VALUE = 1000000
    MIN_THRESHOLD_VALUE = -1000000
