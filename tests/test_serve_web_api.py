import uuid
from unittest.mock import MagicMock, mock_open, patch

from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from B_serve_web_api import (
    app,
    get_available_theme_names,
    is_valid_ticker,
    log_and_raise_error,
)
from tests.test_data.web_api_test_data import (
    companies_by_ticker_bad_request_response,
    companies_by_ticker_not_found_response,
    companies_by_ticker_response,
    company_tickers_by_theme_name_bad_request_response,
    company_tickers_by_theme_name_not_found,
    company_tickers_by_theme_name_response,
    internal_server_error_response,
)

client = TestClient(app)


class TestingGetCompanyByTickerSymbol:
    def testing_200(self):
        response = client.get("/v1/companies/AAPL")
        assert response.status_code == 200
        assert response.json() == companies_by_ticker_response

    def testing_400(self):
        response = client.get("/v1/companies/AABBCCDD")
        assert response.status_code == 400
        assert response.json() == companies_by_ticker_bad_request_response

    def testing_404(self):
        with patch.object(Session, "query", return_value=MagicMock()) as mock_query:
            mock_query.return_value.filter.return_value.all.return_value = []
            response = client.get("/v1/companies/AAPL")
            assert response.status_code == 404
            assert response.json() == companies_by_ticker_not_found_response

    def testing_500(self):
        with patch.object(Session, "query", return_value=MagicMock()) as mock_query:
            mock_query.return_value.filter.side_effect = SQLAlchemyError
            response = client.get("/v1/companies/AAPL")
            assert response.status_code == 500
            assert response.json() == internal_server_error_response


class TestingListCompanyTickersByThemeName:
    def testing_200(self):
        response = client.get("/v1/companies/list-by-theme/manufacturing")
        assert response.status_code == 200
        assert response.json() == company_tickers_by_theme_name_response

    def testing_400(self):
        response = client.get("/v1/companies/list-by-theme/a")
        assert response.status_code == 400
        assert response.json() == company_tickers_by_theme_name_bad_request_response

    def testing_404(self):
        with patch.object(Session, "query", return_value=MagicMock()) as mock_query:
            mock_query.return_value.filter.return_value.all.return_value = []
            response = client.get("/v1/companies/list-by-theme/manufacturing")
            assert response.status_code == 404
            assert response.json() == company_tickers_by_theme_name_not_found

    def testing_500(self):
        with patch.object(Session, "query", return_value=MagicMock()) as mock_query:
            mock_query.return_value.filter.side_effect = SQLAlchemyError
            response = client.get("/v1/companies/list-by-theme/manufacturing")
            assert response.status_code == 500
            assert response.json() == internal_server_error_response


class TestingIsValidTicker:
    def test_return_true(self):
        assert is_valid_ticker("AAA")

    def test_return_false(self):
        assert not is_valid_ticker("AAAAAAA")


class TestingGetAvailableThemeNames:
    def testing_happy_path(self):
        mock_file_content = "theme1\ntheme2\ntheme3\n"

        with patch(
            "builtins.open", mock_open(read_data=mock_file_content)
        ) as mock_file:
            result = get_available_theme_names("fake_path")
            mock_file.assert_called_once_with("fake_path", "r", encoding="utf-8")
            assert result == ["theme1", "theme2", "theme3"]


class TestingLogAndRaiseError:
    def test_log_and_raise_error(self):
        test_uuid = uuid.uuid4()
        test_endpoint = "/test"
        test_error = HTTPException(status_code=123, detail="test")
        with patch("B_serve_web_api.logger.info") as mock_logger:
            try:
                log_and_raise_error(test_uuid, test_endpoint, test_error)
            except HTTPException as e:
                assert e == test_error
            mock_logger.assert_called_once_with(
                f"[{test_uuid}][{test_endpoint}]Endpoint returned error({test_error.status_code}):{test_error.detail}"
            )
