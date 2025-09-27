from sqlmodel import SQLModel, create_engine, Session
from core.config import settings
from contextlib import contextmanager

engine = create_engine(settings.database_url,echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

