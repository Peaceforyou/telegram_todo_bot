from config import connect_sync_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase


sync_engine = create_engine(
    url=connect_sync_url(),
    echo=True
)

sesison_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass