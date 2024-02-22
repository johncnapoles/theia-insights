import json
import re
import uuid
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from constants.web_constants import (
    DOCUMENT_VERSION,
    PATH,
    REGEX_TICKER_PATTERN,
    CompanyDetail,
    CompanyTickerList,
)
from db.database import CompaniesTable, SessionLocal, get_db, initialize_data
from utils.logger import create_logger


def startup_event():
    """Code block that runs on application startup. Used for initializing database"""
    db = SessionLocal()
    initialize_data(db)
    db.close()
    logger.info("Done application startupa and db initialization.")


def log_and_raise_error(
    request_uuid: uuid, endpoint: str, error: HTTPException
) -> None:
    """Helper Function to write errors to log and return an exception to the requester"""
    logger.info(
        f"[{request_uuid}][{endpoint}]Endpoint returned error({error.status_code}):{error.detail}"
    )
    raise error


def is_valid_ticker(ticker: str) -> bool:
    return bool(ticker_pattern.match(ticker))


def get_available_theme_names(path=PATH.THEME_NAMES.value) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        themes = [line.strip() for line in f.readlines() if line.strip() != ""]
    return themes


ticker_pattern = re.compile(REGEX_TICKER_PATTERN)
theme_names = get_available_theme_names()
logger = create_logger("web-api", console_logging=False)
app = FastAPI(version=DOCUMENT_VERSION)
logger.info("STARTED serve_web_api.py")
app.add_event_handler("startup", startup_event)


@app.get("/v1/companies/{ticker}", tags=["Companies"])
async def get_company_by_ticker_symbol(
    ticker: Annotated[str, Path(description="ticker symbol filter")],
    db: Session = Depends(get_db),
) -> CompanyDetail:
    """
    This endpoint will return the company associated with the supplied ticker symbol.
    If found, the response will contain the company's ticker, name, description, and top themes.
    Otherwise, an error will be given.
    """
    endpoint = f"/v1/companies/{ticker}"
    request_uuid = uuid.uuid4()
    logger.info(f"[{request_uuid}][{endpoint}]Endpoint called. Handling request.")

    if not is_valid_ticker(ticker.upper()):
        log_and_raise_error(
            request_uuid,
            endpoint,
            HTTPException(
                status_code=400,
                detail="Invalid ticker. Up to 6 capital letters only.",
            ),
        )

    try:
        filtered_companies = (
            db.query(CompaniesTable)
            .filter(func.upper(CompaniesTable.company_ticker) == ticker.upper())
            .all()
        )
    except Exception:
        log_and_raise_error(
            request_uuid,
            endpoint,
            HTTPException(status_code=500, detail="Internal Server Error."),
        )

    if len(filtered_companies) == 0:
        log_and_raise_error(
            request_uuid,
            endpoint,
            HTTPException(
                status_code=404,
                detail=f"No company found with given ticker: {ticker.upper()}",
            ),
        )

    logger.info(
        f"[{request_uuid}][{endpoint}]Endpoint resolved. Response:{json.dumps(filtered_companies[0].to_json())}"
    )
    return filtered_companies[0]


@app.get("/v1/companies/list-by-theme/{theme}", tags=["Companies"])
async def list_company_tickers_by_theme_name(
    theme: Annotated[str, Path(description="theme name filter")],
    db: Session = Depends(get_db),
) -> CompanyTickerList:
    """
    This endpoint will return a list of companies that contain the same theme names.
    If at least one matches, the response will contain the theme name, the number of matches, and the list of company tickers.
    Otherwise, an error will be given.
    """
    endpoint = f"/v1/companies/list-by-theme/{theme}"
    request_uuid = uuid.uuid4()
    logger.info(f"[{request_uuid}][{endpoint}]Endpoint called. Handling request.")

    if theme.lower() not in theme_names:
        log_and_raise_error(
            request_uuid,
            endpoint,
            HTTPException(
                status_code=400,
                detail=f"invalid theme:{theme}\nAccepted themes:{theme_names}",
            ),
        )

    try:
        filtered_companies = (
            db.query(CompaniesTable)
            .filter(
                func.lower(CompaniesTable.company_top_themes).like(f"%{theme.lower()}%")
            )
            .all()
        )
    except Exception:
        log_and_raise_error(
            request_uuid,
            endpoint,
            HTTPException(status_code=500, detail="Internal Server Error."),
        )

    list_of_tickers = [company.company_ticker for company in filtered_companies]

    if len(list_of_tickers) == 0:
        log_and_raise_error(
            request_uuid,
            endpoint,
            HTTPException(
                status_code=404, detail=f"No companies found with theme name: {theme}"
            ),
        )

    return_object = {
        "theme_name": theme,
        "number_of_matches": len(list_of_tickers),
        "data": list_of_tickers,
    }

    logger.info(
        f"[{request_uuid}][{endpoint}]Endpoint resolved. Response:{json.dumps(return_object)}."
    )
    return return_object
