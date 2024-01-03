from sqlmodel import SQLModel, Session, create_engine 


_engine = create_engine("sqlite:///santa_company.db")


def get_session():
    with Session(_engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(_engine)

