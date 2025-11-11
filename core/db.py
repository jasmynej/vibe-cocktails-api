from sqlmodel import create_engine, SQLModel, Session
from core.config import settings

engine = create_engine(settings.DB_URI)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

def get_sync_session():
    return Session(engine)