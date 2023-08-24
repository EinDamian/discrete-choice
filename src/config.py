import platform
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
    ALTERNATIVE_OVERRIDE_CONFIRMATION = "The label '%s' already exists for an alternative.\nAre you sure you want to override the existing alternative?"
    IMPORT_INVALID_CONFIRMATION = "The following Alternatives are invalid: \n%s \n\nAre you sure you want to continue to import?"
    EXPORT_INVALID_CONFIRMATION = "The following Alternatives are invalid: \n%s \n\nAre you sure you want to continue to export?"


class ConfigColumnWidget:
    """Configuration of the Column Widget"""
    INDEX_LABEL = 0
    INDEX_TYPE = 1
    INDEX_DEFINITION = 2
    HEADERS = ['Label', 'Type', 'Definition']
    BUTTON_NAME_ADDITION = "Add"
    WINDOW_TITLE_ADDITION = "Add new Derivative"
    FILLER_EMPTY_DEFINITION = "-"
    FILLER_UNDETERMINED_DATATYPE = "?"
    FILE_TYPE_FILTER_DERIVATIVE_IMPORT = "Text files (*.json)"
    DERIVATIVE_IMPORT_WINDOW_TITLE = "Select Derivative Files for Import:"
    DERIVATIVE_EXPORT_WINDOW_TITLE = "Choose a path to export derivative:"
    DERIVATIVE_OVERRIDE_CONFIRMATION = "A derivative with label '%s' already exists.\nAre you sure you want to override the existing derivative?"
    RAW_DATA_OVERRIDE_CONFIRMATION = "An attribute with the same label already exists.\nDerivatives with the same name as attributes can not be added. \nDo you want to save it as '%s' instead?"
    LABEL_OVERRIDE_AVOIDANCE_CHARACTER = "_2"
    IMPORT_INVALID_CONFIRMATION = "The following Derivatives are invalid: \n%s \n\nAre you sure you want to continue to import?"
    EXPORT_INVALID_CONFIRMATION = "The following Derivatives are invalid: \n%s \n\nAre you sure you want to continue to export?"


class ConfigFunctionHighlighting:
    """Configurations of the Highlighting of Functions with errors"""
    OPACITY = 128
    MISTAKE_TOOLTIP_START = "Found Mistakes:\n"
    LIST_CHARACTER_MISTAKES_TOOLTIP = "\n\u2022"
    MISSING_EXPRESSION_HIGHLIGHTING_WIDTH = 100

    # highlighting offset is os dependent
    match platform.system():
        case "Windows": HIGHLIGHTING_OFFSET = 3
        case "Darwin": HIGHLIGHTING_OFFSET = 5
        case _: HIGHLIGHTING_OFFSET = 5


class ConfigFileManagementWindow:
    """ Configuration of FileManagementWindow"""
    DIR_FILE_EXTENSIONS = '.dir'
    LAST_FOURTH_POSITION = -4


class ConfigFileMenu:
    """ Configuration of the FileMenu"""
    OPEN_PROJECT_DIALOG_TITLE = 'Open Project'
    SAVE_PROJECT_DIALOG_TITLE = 'Save Project'
    SAVE_PROJECT_AS_DIALOG_TITLE = 'Save Project As'
    IMPORT_DATA_DIALOG_TITLE = 'Import Data'
    EXPORT_DATA_DIALOG_TITLE = 'Export To'
    DIRECTORY_FILE_FORMAT = 'Directory (*.dir)'
    CSV_FILE_FORMAT = 'CSV File (*.csv)'
    WARNING_DIALOG_TITLE = 'Warning!'
    MESSAGE_DIALOG_SAVE_BEFORE_NEW = 'Do you wish to save the project before opening a new one?'
    MESSAGE_DIALOG_SAVE_BEFORE_OTHER = 'Do you wish to save the project before opening another one?'


class ConfigEvaluationWidget:
    """Configuration of the EvaluationWidget"""
    EXPORT_DIALOG_TITLE = 'Export File'
    CSV_FILE_FORMAT = 'CSV File (*.csv)'


class ConfigThresholdWindow:
    """ Configuration of ThresholdWindow"""
    FIELD_MIN_WIDTH = 200
    FIELD_MIN_HEIGHT = 0
    NUM_OF_STRETCH = 1
    DEFAULT_THRESHOLD = 0


class ConfigThresholdField:
    """ Configuration of ThresholdField"""
    MAX_THRESHOLD_VALUE = 1000000
    MIN_THRESHOLD_VALUE = -1000000


class ConfigProjectManager:
    EVALUATION = "evaluation.csv"
    CONFIG = "config.json"
    CHOICE = "Choice.json"
    RAW_DATA_PATH = "raw_data_path.json"
    ALTERNATIVES = "alternatives"
    DERIVATIVES = "derivatives"
    THRESHOLDS = "thresholds"
    PROCESSING_CONFIGS = "processing_configs"


class ConfigProcessingWidget:
    HEADERS = ['Variable', 'Value']
    CHOICE = "$CHOICE"
    

class ConfigUserInputWindow:
    """Configuration of the User Input Window for the Functions"""
    SYNTAX_HELP = """Syntax rules for the Addition of Derivatives and Alternatives:
    \n Definition: The function that the derivative/ alternative represents. To represent attributes or other variables use their label. The function should follow Python syntax:
    \n \t Mathematical Operations: +, -, *, /, %, abs, divmod, max, min, pow, range, set, sum
    \n \t Logical Operation: True, False, None, and, or, not, ==, <, >, >=, <=, !=
    \n \t Supported Characters: a-z, A-Z, 0-9, (, )
    \n \t Other Operations: Interval(), GroupMap()
    \n
    \n Labels: The name of the Attribute. Labels have to start with a letter and can only contain the following characters: a-z, A-Z, 0-9, _
    \n The Labels should not have the name of one of the Operations mentioned above. Labels can only refer to one Derivative or Alternative.
    \n Choice Index: An integer necessary to calculate the discrete choice model. For n Alternatives the choice indexes from 0 to n-1 need to exist.
    \n
    \n For further Information consult the Manual through the Help Menu.
    """