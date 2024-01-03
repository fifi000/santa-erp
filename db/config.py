import os

from sqlmodel import SQLModel, Session, create_engine 

conn = os.getenv('DB_URL')
if not conn:
    raise Exception('`DB_URL` environment variable is not set')

_engine = create_engine(conn)


def get_session():
    with Session(_engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(_engine)

