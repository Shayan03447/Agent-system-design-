# Engine + SessionLocal for SQLAlchemy

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import URL, make_url
from dotenv import load_dotenv
import os

# ---Get the postgress url from the envirnoment variables
load_dotenv()
DATABASE_URL= (os.getenv("POSTGRESS_Url") or "").strip()
if not DATABASE_URL:
    raise RuntimeError("Postgress_url is not set")

try:
    parsed_url: URL = make_url(DATABASE_URL)
except Exception as exc:
    raise RuntimeError(
        "POSTGRES_URL is invalid. Expected format like"
        "'postgresql+psycopg2://user:password@host:5432/dbname'"
        )from exc
   


if not parsed_url.drivername.startwith("postgresql"):
    raise RuntimeError(f"Postgress_url must use a postgreSQL driver, got '{parsed_url.drivername}'.")
# Keep SQL Logs disabled by default in production
SQL_ECHO = os.getenv("SQL_ECHO", "false").strip().lower()=="true"

# ENGINE FOR THE DATABASE
engine=create_engine(
    DATABASE_URL,
    echo=SQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)

# Session local for the database
SessionLocal=sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
)

# get_db function used in every API call
def get_db()-> Generator[Session, None, None]:
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()