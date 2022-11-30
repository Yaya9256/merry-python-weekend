from contextlib import contextmanager
from sqlalchemy import create_engine
from database import table_model
from read_config import get_db_info

username = get_db_info()["USERNAME"]
pwd = get_db_info()["PASSWORD"]
host = get_db_info()["HOST"]
port = get_db_info()["PORT"]
dbname = get_db_info()["DB"]

CONNECTION_STRING = f"postgresql://{username}:{pwd}@{host}:{port}/{dbname}"

engine = create_engine(
    CONNECTION_STRING,
    pool_size=1,
    max_overflow=0,
    echo=True,
    )


@contextmanager
def database_connection():
    with engine.connect() as connection:
        yield connection


def create_tables_on_startup():
    table_model.metadata.create_all(engine)
