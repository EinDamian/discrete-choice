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


class ConfigExpressionErrors:
    """Configuration of errors associated with FunctionalExpressions"""
    COLOR_HEX = 0x0


class ConfigRegexPatterns:
    """Configuration of used regex patterns"""
    PATTERN_FUNCTION_LABEL = "^[a-zA-Z]+[a-zA-Z0-9_]*$"
    PATTERN_DATATYPES = "[a-zA-Z]+"


class ConfigFiles:
    """Configuration of path strings"""
    PATH_JSON_FILE = "%s/%s.json"
    SEPARATOR_CSV = ";"


class ConfigModelWidget:
    """Configuration of the Model Widget"""
    INDEX_LABEL = 0
    INDEX_DEFINITION = 1
    INDEX_AVAILABILITY = 2
    HEADERS = ['Label', 'Definition', 'Availability Condition']
    BUTTON_NAME_ADDITION = "Add"
    WINDOW_TITLE_ADDITION = "Add new Alternative:"
    FILE_TYPE_FILTER_ALTERNATIVE_IMPORT = "Text files (*.json)"


class ConfigColumnWidget:
    """Configuration of the Column Widget"""
    INDEX_LABEL = 0
    INDEX_TYPE = 1
    INDEX_DEFINITION = 2
    HEADERS = ['Label', 'Type', 'Definition']
    FILLER_EMPTY_DEFINITION = "-"
    FILE_TYPE_FILTER_DERIVATIVE_IMPORT = "Text files (*.json)"


class ConfigFunctionHighlighting:
    """Configurations of the Highlighting of Functions with errors"""
    OPACITY = 128
    MISTAKE_TOOLTIP_START = "Found Mistakes:\n"
    LIST_CHARACTER_MISTAKES_TOOLTIP = "\n\u2022"
