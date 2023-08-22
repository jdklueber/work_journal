from sqlalchemy import create_engine
from work_journal.core.db import Base


def create_new_test_engine():
    return create_engine("sqlite://")


def create_new_test_db(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_clean_db():
    engine = create_new_test_engine()
    create_new_test_db(engine)
    return engine
