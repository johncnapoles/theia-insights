from enum import Enum

MODEL_NAME = "flax-sentence-embeddings/all_datasets_v4_MiniLM-L6"


class FORMAT(Enum):
    """
    Constants related to any regular expressions for validation
    """

    THEME_NAME = r"^[a-zA-Z0-9][a-zA-Z0-9-.#&]*[a-zA-Z0-9]$"
    HTML_TAG_STRUCTURE = ["html", "head", "title", "body", "h1", "h2", "p"]


class PATH(Enum):
    """
    Constants Related to path of inputs and outputs
    """

    INPUT_THEME_FILE = "inputs/themes.txt"
    INPUT_COMPANIES_DIRECTORY = "inputs/companies"
    OUTPUT_DIRECTORY = "outputs/"
    LOG_DIRECTORY = "logs"
    OUTPUT_THEME_NAMES_FILE = "outputs/theme_names.txt"


class PREFIX(Enum):
    """
    Formatting prefixes to identify substrings in HTML data
    """

    TITLE_NAME = "Company Description:"
    TICKER = "Ticker:"


class ERROR(Enum):
    """
    Constants related to Warning messages for defesnive programming
    """

    # Related to Theme txt file pre-processing
    THEME_MISSING_COLON = (
        """expected format: "theme name <colon> theme description". missing colon"""
    )
    THEME_MISSING_NAME = (
        """expected format: "theme name <colon> theme description". missing name"""
    )
    THEME_MISSING_DESCRIPTION = """expected format: "theme name <colon> theme description". missing description"""
    THEME_NAME_REGEX = (
        """Theme name must follow the regex '[a-zA-Z0-9][a-zA-Z0-9-.#&]*[a-zA-Z0-9]'"""
    )
    NO_THEMES = "no themes parsed. exiting program because there are no themes to compare companies with."
    # Related to Company HTML file pre-processing
    HTML_MALFORMED_DATA = "HTML is not in expected format. The file will be skipped."
    HTML_BLANK_COMPANY_NAME = (
        "Company name is missing from BODY->H1. Please fix. The file will be skipped."
    )
    HTML_MISSING_TITLE_PREFIX = """TITLE is expected in the format "Company Description: <Company name>". Please fix. The file will be skipped."""
    HTML_MISMATCH_NAME = (
        "Company name in BODY->H1 mismatch TITLE. Please fix. The file will be skipped."
    )
    HTML_MISSING_TICKER_PREFIX = "Company ticker (expected in BODY->H2) is missing."
    HTML_BLANK_COMPANY_TICKER = "Company ticker (expected in BODY->H2) is blank"
    HTML_BLANK_COMPANY_DESCRIPTION = (
        "Company description (expected in BODY->P) is blank."
    )
    NO_COMPANIES = "no companies parsed. exiting program because there are no companies to identify themes for."
