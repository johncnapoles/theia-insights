from typing import List
from pydantic import BaseModel, Field
from enum import Enum

DOCUMENT_VERSION = "1.0.0"

REGEX_TICKER_PATTERN = r"^[A-Z]{1,6}$"


class PATH(Enum):
    """
    Constants path of data sources
    """

    PROCESSED_DATA = "outputs/output.jsonl"
    THEME_NAMES = "outputs/theme_names.txt"


class CompanyDetail(BaseModel):
    company_ticker: str = Field(
        title="company ticker", description="the company's ticker symbol."
    )
    company_name: str = Field(title="company name", description="the company's name.")
    company_top_themes: str = Field(
        title="company top themes", description="the top themes of the company."
    )
    company_description: str = Field(
        title="company description",
        description="the description about the company's position in its industries",
    )


class CompanyTickerList(BaseModel):
    theme_name: str = Field(
        title="theme name", description="the theme name supplied in the request path."
    )
    number_of_matches: int = Field(
        title="number of matches",
        description="the number of companies that have the theme name in.",
    )
    data: List[str] = Field(
        title="data",
        description="the list of companies by ticker symbol where the theme matches the company's top themes.",
    )
