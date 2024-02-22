import logging
import re
from unittest.mock import MagicMock, mock_open, patch

from torch import Tensor
import pytest
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

from A_process_data_pipeline import (
    determine_themes,
    extract_company_description,
    extract_company_details,
    extract_company_name,
    extract_company_ticker,
    extract_theme_details,
    is_expected_html_format,
    is_valid_theme_name,
    parse_company_files,
    parse_themes,
    process_list_of_companies,
    read_lines_from_file,
)
from constants.data_constants import ERROR
from tests.test_data.data_pipeline_test_data import (
    sample_determine_themes_output,
    sample_processed_companies,
    sample_processed_themes,
    test_company_blank_company_name,
    test_company_blank_description,
    test_company_blank_ticker_prefix,
    test_company_description,
    test_company_html,
    test_company_html_no_ticker,
    test_company_mismatch_name,
    test_company_missing_ticker_prefix,
    test_company_missing_title_prefix,
    test_invalid_html_format,
    test_parse_themes_output,
)


class TestingParseThemes:
    def testing_parse_themes(self):
        mock_logger = MagicMock(spec=logging.Logger)
        mock_model = MagicMock(spec=SentenceTransformer)
        mock_model.encode.return_value = "test encode value"

        test_output_read_line_from_files = [
            "theme1: description1",
            "theme2: description2",
        ]
        test_output_extract_theme_details = [
            ("theme1", "description1"),
            ("theme2", "description2"),
        ]

        expected_log_info = (
            "Done parsing themes. There are 2 themes: ['theme1', 'theme2']"
        )

        with patch(
            "A_process_data_pipeline.read_lines_from_file",
            return_value=test_output_read_line_from_files,
        ), patch(
            "A_process_data_pipeline.extract_theme_details",
            side_effect=test_output_extract_theme_details,
        ):
            result = parse_themes(mock_logger, mock_model)
            assert result == test_parse_themes_output
            mock_logger.info.assert_called_once_with(expected_log_info)


class TestingReadLinesFromFile:
    def test_with_file_input(self):
        result = read_lines_from_file("tests/test_data/sample_theme_file.txt")
        assert len(result) == 3

    def test_with_mocked_input(self):
        mocked_file_content = "Line1\nLine2\n\nLine4"
        expected_result = ["Line1", "Line2", "Line4"]
        with patch("builtins.open", mock_open(read_data=mocked_file_content)):
            result = read_lines_from_file("fake/fakepath.txt")
        assert result == expected_result


class TestingExtractThemeDetails:
    theme_name_pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-.#&]*[a-zA-Z0-9]$")

    def testing_happy_path(self):
        test_input = "theme-name:theme description text."
        expected_theme_name = "theme-name"
        expected_theme_output = "theme description text."

        theme_name, theme_description = extract_theme_details(
            test_input, self.theme_name_pattern
        )
        assert theme_name == expected_theme_name
        assert theme_description == expected_theme_output

    def testing_missing_colon_exception(self):
        test_input = "theme-nametheme description text."
        expected_error_message = f"{ERROR.THEME_MISSING_COLON.value}: {test_input}"
        with pytest.raises(Exception) as error:
            extract_theme_details(test_input, self.theme_name_pattern)
        assert str(error.value) == expected_error_message

    def testing_missing_theme_name(self):
        test_input = ":theme description."
        expected_error_message = f"{ERROR.THEME_MISSING_NAME.value}: {test_input}"
        with pytest.raises(Exception) as error:
            extract_theme_details(test_input, self.theme_name_pattern)
        assert str(error.value) == expected_error_message

    def testing_missing_theme_description(self):
        test_input = "theme-name:"
        expected_error_message = (
            f"{ERROR.THEME_MISSING_DESCRIPTION.value}: {test_input}"
        )
        with pytest.raises(Exception) as error:
            extract_theme_details(test_input, self.theme_name_pattern)
        assert str(error.value) == expected_error_message

    def testing_theme_name_regex(self):
        test_input = "@theme-name:theme-description"
        expected_error_message = f"{ERROR.THEME_NAME_REGEX.value}: {test_input}"
        with pytest.raises(Exception) as error:
            extract_theme_details(test_input, self.theme_name_pattern)
        assert str(error.value) == expected_error_message


class TestingIsValidThemeName:
    theme_name_pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-.#&]*[a-zA-Z0-9]$")

    def testing_match(self):
        test_theme_name = "test-theme"
        assert is_valid_theme_name(test_theme_name, self.theme_name_pattern)

    def testing_no_match(self):
        test_theme_name = "!hello-theme"
        assert not is_valid_theme_name(test_theme_name, self.theme_name_pattern)


class TestingParseCompanyFiles:
    def test_parse_company_files(self):
        mock_logger = MagicMock(spec=logging.Logger)
        mock_model = MagicMock(spec=SentenceTransformer)
        expected_test_output = {
            "company1": {},
            "company2": {},
            "company3": {},
        }
        expected_log_info = "Done parsing companies. There are 3 companies. Last three: ['company1', 'company2', 'company3']"

        with patch(
            "os.listdir", return_value=["file1.html", "file2.html", "file3.html"]
        ), patch(
            "A_process_data_pipeline.process_list_of_companies",
            return_value={"company1": {}, "company2": {}, "company3": {}},
        ):
            result = parse_company_files(mock_logger, mock_model)
            assert result == expected_test_output
            mock_logger.info.assert_called_once_with(expected_log_info)


class TestingProcessListOfCompanies:
    def test_happy_path(self):
        mock_logger = MagicMock(spec=logging.Logger)
        mock_model = MagicMock(spec=SentenceTransformer)
        mock_model.encode.return_value = "test encode value"

        open_file_test_output = "html content"
        beautiful_soup_test_output = "processed html"
        is_expected_html_format_test__output = True
        extract_company_details_test_output = (
            "company name",
            "company ticker",
            "company description",
        )

        test_list_of_html_files = ["file1.html", "file2.html"]

        expected_result = {
            "company ticker": {
                "company_name": "company name",
                "company_ticker": "company ticker",
                "company_description": "company description",
                "company_description_model_encoding": "test encode value",
            }
        }

        with patch("builtins.open", mock_open(read_data=open_file_test_output)), patch(
            "bs4.BeautifulSoup", return_value=beautiful_soup_test_output
        ), patch(
            "A_process_data_pipeline.is_expected_html_format",
            return_value=is_expected_html_format_test__output,
        ), patch(
            "A_process_data_pipeline.extract_company_details",
            return_value=(extract_company_details_test_output),
        ):
            companies = process_list_of_companies(
                mock_logger, test_list_of_html_files, mock_model
            )
            assert companies == expected_result


class TestingIsExpectedHtmlFormat:
    def testing_expected_html(self):
        test_data = BeautifulSoup(test_company_html, "html.parser")
        assert is_expected_html_format(test_data)

    def testing_unexpected_html(self):
        test_data = BeautifulSoup(test_invalid_html_format, "html.parser")
        assert not is_expected_html_format(test_data)


class TestingExtractCompanyDetails:
    def testing_happy_path(self):
        test_data = BeautifulSoup(test_company_html, "html.parser")
        expected_name = "Apple Inc."
        expected_ticker = "AAPL"
        expected_description = test_company_description
        name, ticker, description = extract_company_details(test_data)
        assert name == expected_name
        assert ticker == expected_ticker
        assert description == expected_description

    def testing_exception_path(self):
        test_data = BeautifulSoup(test_company_html_no_ticker, "html.parser")
        expected_error_message = f"{ERROR.HTML_MISSING_TICKER_PREFIX.value}"
        with pytest.raises(Exception) as error:
            extract_company_details(test_data)
        assert str(error.value) == expected_error_message


class TestingExtractCompanyName:
    def testing_happy_path(self):
        test_data = BeautifulSoup(test_company_html, "html.parser")
        expected_name = "Apple Inc."
        name = extract_company_name(test_data)
        assert name == expected_name

    def testing_blank_company_name(self):
        test_input = BeautifulSoup(test_company_blank_company_name, "html.parser")
        expected_error_message = f"{ERROR.HTML_BLANK_COMPANY_NAME.value}"
        with pytest.raises(Exception) as error:
            extract_company_name(test_input)
        assert str(error.value) == expected_error_message

    def testing_missing_title_prefix(self):
        test_input = BeautifulSoup(test_company_missing_title_prefix, "html.parser")
        expected_error_message = f"{ERROR.HTML_MISSING_TITLE_PREFIX.value}"
        with pytest.raises(Exception) as error:
            extract_company_name(test_input)
        assert str(error.value) == expected_error_message

    def testing_mismatch_name(self):
        test_input = BeautifulSoup(test_company_mismatch_name, "html.parser")
        expected_error_message = f"{ERROR.HTML_MISMATCH_NAME.value}"
        with pytest.raises(Exception) as error:
            extract_company_name(test_input)
        assert str(error.value) == expected_error_message


class TestingExtractCompanyTicker:
    def testing_happy_path(self):
        test_data = BeautifulSoup(test_company_html, "html.parser")
        expected_ticker = "AAPL"
        ticker = extract_company_ticker(test_data)
        assert ticker == expected_ticker

    def testing_missing_ticker_prefix(self):
        test_input = BeautifulSoup(test_company_missing_ticker_prefix, "html.parser")
        expected_error_message = f"{ERROR.HTML_MISSING_TICKER_PREFIX.value}"
        with pytest.raises(Exception) as error:
            extract_company_ticker(test_input)
        assert str(error.value) == expected_error_message

    def testing_blank_ticker(self):
        test_input = BeautifulSoup(test_company_blank_ticker_prefix, "html.parser")
        expected_error_message = f"{ERROR.HTML_BLANK_COMPANY_TICKER.value}"
        with pytest.raises(Exception) as error:
            extract_company_ticker(test_input)
        assert str(error.value) == expected_error_message


class TestingExtractCompanyDescription:
    def testing_happy_path(self):
        test_data = BeautifulSoup(test_company_html, "html.parser")
        expected_description = test_company_description
        description = extract_company_description(test_data)
        assert description == expected_description

    def testing_blank_company_description(self):
        test_input = BeautifulSoup(test_company_blank_description, "html.parser")
        expected_error_message = f"{ERROR.HTML_BLANK_COMPANY_DESCRIPTION.value}"
        with pytest.raises(Exception) as error:
            extract_company_description(test_input)
        assert str(error.value) == expected_error_message


class TestingDetermineThemes:
    def testing_determine_themes(self):
        mock_logger = MagicMock(spec=logging.Logger)
        themes = sample_processed_themes
        companies = sample_processed_companies

        expected_log_info = "Done determining top 1 themes for every company."

        mock_cos_similarity_result = MagicMock(spec=Tensor)
        mock_cos_similarity_result.item.return_value = 1

        with patch(
            "sentence_transformers.util.pytorch_cos_sim",
            return_value=mock_cos_similarity_result,
        ):
            result = determine_themes(mock_logger, themes, companies, topNThemes=1)
            assert result == sample_determine_themes_output
            mock_logger.info.assert_called_once_with(expected_log_info)
