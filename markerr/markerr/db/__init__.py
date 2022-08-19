import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = ("Base", "Session")


log = logging.getLogger(__name__)

metadata = sqlalchemy.MetaData(
    naming_convention={
        "ix": "ix__%(column_0_label)s",
        "uq": "uq__%(table_name)s__%(column_0_name)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        "fk": "fk__%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
        "pk": "pk__%(table_name)s",
    }
)

Base = declarative_base(metadata=metadata)
Session = sessionmaker()


def init(engine, base=Base, drop_all=False, create_all=False):
    import markerr.models

    if drop_all:
        log.info("dropping all tables")
        base.metadata.reflect(engine)
        base.metadata.drop_all(engine)
    if create_all:
        log.info("creating all tables")
        engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        base.metadata.create_all(engine)


def create_engine(database_uri):
    return sqlalchemy.create_engine(database_uri)
