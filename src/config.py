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
    COLOR_HEX = 0xFF3030

    ERROR_INVALID_SYNTAX = "Invalid syntax."
    ERROR_BRACKET_NOT_CLOSED = "Bracket was never closed."
    ERROR_UNMATCHED_BRACKET = "Bracket was never opened."

    ERROR_VARIABLE_NON_EXISTENT = "Variable name '{0}' does not exist."
    ERROR_CYCLIC_DEPENDENCY = "Variable leads to cyclic dependency: {0}."
    ERROR_INVALID_VARIABLE = "Variable '{0}' is not valid."

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


class ConfigEvaluationWidget:
    EXPORT_DIALOG_TITLE = 'Export File'
    DIRECTORY_FILE_FORMAT = 'Directory (*.dir)'


class ConfigThresholdWindow:
    FIELD_MIN_WIDTH = 200
    FIELD_MIN_HEIGHT = 0
    NUM_OF_STRETCH = 1


class ConfigThresholdField:
    MAX_THRESHOLD_VALUE = 1000000
    MIN_THRESHOLD_VALUE = -1000000
