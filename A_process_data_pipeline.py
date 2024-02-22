import logging
import re
import sys
from os import listdir
from typing import Dict, List, Pattern

import jsonlines
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util

from constants.data_constants import ERROR, FORMAT, MODEL_NAME, PATH, PREFIX
from utils.logger import create_logger


def parse_themes(logger: logging.Logger, model: SentenceTransformer) -> Dict[str, any]:
    """Reads lines from input themes.txt file, processes every line with a helper function and returns
    a dictionary of processed themes.
    """
    themes = dict()
    theme_name_pattern = re.compile(FORMAT.THEME_NAME.value)

    lines = read_lines_from_file(PATH.INPUT_THEME_FILE.value)

    for line in lines:
        try:
            theme_name, theme_description = extract_theme_details(
                line, theme_name_pattern
            )
        except Exception as error_message:
            logger.error(error_message)
            continue

        themes[theme_name] = {
            "theme_name": theme_name,
            "theme_description": theme_description,
            "theme_description_model_encoding": model.encode(
                theme_description, convert_to_tensor=True
            ),
        }

    logger.info(
        f"Done parsing themes. There are {len(themes)} themes: {list(themes.keys())}"
    )

    if len(themes) < 1:
        logger.error(ERROR.NO_THEMES.value)
        sys.exit()

    return themes


def read_lines_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip() != ""]


def extract_theme_details(line: str, theme_name_pattern: Pattern) -> tuple:
    """Extracts and returns the theme name and theme description from a given string.
    Raise exceptions for malformed data.

    Note: the specification states the format is: theme name <colon> theme description
    """
    index_colon = line.find(":")
    if index_colon == -1:
        raise Exception(f"{ERROR.THEME_MISSING_COLON.value}: {line[:100]}")
    theme_name = line[:index_colon].strip().lower().replace(" ", "-")
    theme_description = line[index_colon + 1 :].strip()

    if not theme_name:
        raise Exception(f"{ERROR.THEME_MISSING_NAME.value}: {line[:100]}")
    if not theme_description:
        raise Exception(f"{ERROR.THEME_MISSING_DESCRIPTION.value}: {line[:100]}")
    if not is_valid_theme_name(theme_name, theme_name_pattern):
        raise Exception(f"{ERROR.THEME_NAME_REGEX.value}: {line[:100]}")

    return theme_name, theme_description


def is_valid_theme_name(theme_name: str, theme_name_pattern: Pattern) -> bool:
    return bool(theme_name_pattern.match(theme_name))


def parse_company_files(
    logger: logging.Logger, model: SentenceTransformer
) -> Dict[str, any]:
    """List all html files in the input directory and call helper function to process the list"""
    full_list_of_company_html_files: List[str] = [
        file
        for file in listdir(PATH.INPUT_COMPANIES_DIRECTORY.value)
        if ".html" in file
    ]

    companies: Dict[str, any] = process_list_of_companies(
        logger, full_list_of_company_html_files, model
    )

    company_count = len(companies)
    last_three_companies = [
        company for company in list(companies.keys())[-3:] if company_count > 0
    ]
    logger.info(
        f"Done parsing companies. There are {company_count} companies. Last three: {last_three_companies}"
    )

    if len(companies) < 1:
        logger.error(ERROR.NO_COMPANIES.value)
        sys.exit()

    return companies


def process_list_of_companies(
    logger: logging.Logger, list_of_html_files: List[str], model: SentenceTransformer
) -> Dict[str, any]:
    """Traverse every file in a list, process its contents for company information, then store and
    return as a dictionary
    """

    companies = dict()

    for html_file in list_of_html_files:
        with open(
            f"{PATH.INPUT_COMPANIES_DIRECTORY.value}/{html_file}", "r", encoding="utf-8"
        ) as file:
            html_content = file.read()
            processed_html = BeautifulSoup(html_content, "html.parser")

            if not is_expected_html_format(processed_html):
                logger.error(
                    f"[{PATH.INPUT_COMPANIES_DIRECTORY.value}/{html_file}]:{ERROR.HTML_MALFORMED_DATA.value}"
                )
                continue

            try:
                (
                    company_name,
                    company_ticker,
                    company_description,
                ) = extract_company_details(processed_html)
            except Exception as exception_message:
                logger.error(
                    f"[{PATH.INPUT_COMPANIES_DIRECTORY.value}/{html_file}]:{exception_message}"
                )
                continue

            companies[company_ticker] = {
                "company_name": company_name,
                "company_ticker": company_ticker,
                "company_description": company_description,
                "company_description_model_encoding": model.encode(
                    company_description, convert_to_tensor=True
                ),
            }
    return companies


def is_expected_html_format(processed_html: BeautifulSoup) -> bool:
    """Return boolean if the tag structure is the same expected structure"""
    list_of_tags = [tag.name for tag in processed_html.find_all()]
    if list_of_tags != FORMAT.HTML_TAG_STRUCTURE.value:
        return False
    return True


def extract_company_details(processed_html: BeautifulSoup) -> tuple:
    """Call helper functions to obtain the respective company information and return the tuple of
    information, otherwise raise exception.
    """
    try:
        company_name = extract_company_name(processed_html)
        company_ticker = extract_company_ticker(processed_html)
        company_description = extract_company_description(processed_html)
    except Exception as error_message:
        raise Exception(error_message)

    return company_name, company_ticker, company_description


def extract_company_name(processed_html: BeautifulSoup):
    """Return the company name from where it is expected in HTML, otherwise raise exception."""
    company_name_from_h1 = processed_html.body.h1.text
    if not company_name_from_h1:
        raise Exception(ERROR.HTML_BLANK_COMPANY_NAME.value)

    title_line = processed_html.head.title.text
    index_start_of_name = title_line.find(PREFIX.TITLE_NAME.value)
    if index_start_of_name == -1:
        raise Exception(ERROR.HTML_MISSING_TITLE_PREFIX.value)

    name_from_title = title_line[
        index_start_of_name + len(PREFIX.TITLE_NAME.value) :
    ].strip()
    if name_from_title != company_name_from_h1:
        raise Exception(ERROR.HTML_MISMATCH_NAME.value)

    return company_name_from_h1


def extract_company_ticker(processed_html: BeautifulSoup):
    """Return the company ticker from where it is expected in HTML, otherwise raise exception."""
    company_ticker_line = processed_html.body.h2.text
    index_ticker = company_ticker_line.find(PREFIX.TICKER.value)

    if index_ticker == -1:
        raise Exception(ERROR.HTML_MISSING_TICKER_PREFIX.value)

    company_ticker = (
        company_ticker_line[index_ticker + len(PREFIX.TICKER.value) :].strip().upper()
    )

    if not company_ticker:
        raise Exception(ERROR.HTML_BLANK_COMPANY_TICKER.value)

    return company_ticker


def extract_company_description(processed_html: BeautifulSoup):
    """Return the company description from where it is expected in HTML, otherwise raise exception."""
    company_description_line = processed_html.body.p.text
    company_description = " ".join(
        [line.strip() for line in company_description_line.split("\n")]
    ).strip()

    if not company_description:
        raise Exception(ERROR.HTML_BLANK_COMPANY_DESCRIPTION.value)

    return company_description


def determine_themes(
    logger: logging.Logger,
    themes: Dict[str, any],
    companies: Dict[str, any],
    topNThemes: int = 3,
) -> Dict[str, any]:
    """Given the processed themes and companies, find the cosine similarity between every company
    and every theme. Return a dictionary with all the processed company information and the top N
    themes (highest tensor values)
    """
    companies_with_themes = dict()
    for company_ticker, company in companies.items():
        theme_similarities = {}

        for theme_name, theme in themes.items():
            similarity = util.pytorch_cos_sim(
                company["company_description_model_encoding"],
                theme["theme_description_model_encoding"],
            ).item()
            theme_similarities[theme_name] = similarity

        top_n_themes = [
            theme_tuple[0]
            for theme_tuple in sorted(theme_similarities.items(), key=lambda x: -x[1])[
                :topNThemes
            ]
        ]

        companies_with_themes[company_ticker] = {
            "company_ticker": company_ticker,
            "company_name": company["company_name"],
            "company_top_themes": top_n_themes,
            "company_description": company["company_description"],
        }

    logger.info(f"Done determining top {topNThemes} themes for every company.")
    return companies_with_themes


def save_processed_data_jsonl(
    logger: logging.Logger, companies_with_themes: Dict[str, any]
) -> None:
    """Saves the processed companies with their top themes as a jsonl file"""
    json_lines = companies_with_themes.values()
    with jsonlines.open(f"{PATH.OUTPUT_DIRECTORY.value}/output.jsonl", "w") as writer:
        writer.write_all(json_lines)
    logger.info("Done saving processed company data.")


def save_theme_names(logger: logging.Logger, d: Dict[str, any], file_path: str) -> None:
    """Saves the processed themes as a file with theme_name for every line"""
    content = "\n".join(list(d.keys()))
    with open(file_path, "w") as file:
        file.write(content)
    logger.info(f"Done saving keys of themes into: {file_path}")


def main() -> None:
    logger = create_logger("data-pipeline")
    logger.info("STARTED process_data_pipeline.py")
    model = SentenceTransformer(MODEL_NAME)

    themes = parse_themes(logger, model)
    companies = parse_company_files(logger, model)

    save_theme_names(logger, themes, PATH.OUTPUT_THEME_NAMES_FILE.value)

    companies_with_themes = determine_themes(logger, themes, companies)
    save_processed_data_jsonl(logger, companies_with_themes)
    logger.info("FINISHED process_data_pipeline.py")


if __name__ == "__main__":
    main()
