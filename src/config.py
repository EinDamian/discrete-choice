"""Module containing all the hardcoded variables"""


class ConfigErrorMessages:
    """Configuration of displayed error messages"""
    ERROR_MSG_IMPORT_PATH = "Chosen Path for import does not exist."
    ERROR_MSG_FUNCTION_LABEL_INVALID = "The added label is invalid.\nLabels have to start with a letter and can only contain the following characters: {[a-zA-Z0-9_]}"


class ConfigRegexPatterns:
    """Configuration of used regex patterns"""
    PATTERN_FUNCTION_LABEL = "^[a-zA-Z]+[a-zA-Z0-9_]*$"


class ConfigFiles:
    """Configuration of path strings"""
    PATH_JSON_FILE = "%s/%s.json"
    SEPARATOR_CSV = ";"
