from constants.web_constants import PATH
import json

import jsonlines
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

# Define a database
engine = create_engine(
    "sqlite:///db/companies.db", connect_args={"check_same_thread": False}, echo=False
)

# Define a declarative base
Base = declarative_base()


# Define a model class, which is essentially the table
class CompaniesTable(Base):
    __tablename__ = "companies"
    company_ticker = Column(String, nullable=False, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    company_top_themes = Column(String, nullable=False)
    company_description = Column(String, nullable=False)

    def to_json(self):
        return {
            "company_ticker": self.company_ticker,
            "company_name": self.company_name,
            "company_top_themes": self.company_top_themes,
            "company_description": self.company_description,
        }


# Drop and create the database tables
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def initialize_data(db: Session):
    """
    Helper function to initialize the database with data from the data pipeline on app startup
    """
    try:
        with jsonlines.open(PATH.PROCESSED_DATA.value, "r") as file:
            for line in file:
                line["company_top_themes"] = json.dumps(line["company_top_themes"])
                db.merge(CompaniesTable(**line))
        db.commit()
        db.close()
    except Exception as e:
        db.rollback()
        print(f"Error during initalization: {e}")


def get_db():
    """
    Helper function that endpoint methods use to access the database
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
