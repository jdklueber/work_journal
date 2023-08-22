from datetime import datetime, timedelta
import pytest
from work_journal.core.db import Journal, JournalRepo
from sqlalchemy.orm import Session
from sqlalchemy import select
from .test_db import get_clean_db


@pytest.fixture
def today() -> datetime:
    return datetime.today()


@pytest.fixture
def yesterday(today: datetime) -> datetime:
    return today + timedelta(days=-1)


@pytest.fixture
def engine():
    return get_clean_db()


@pytest.fixture
def repo(engine) -> JournalRepo:
    return JournalRepo(engine)


def test_create(engine, repo):
    actual = repo.create_journal_entry("Hello, world")

    with Session(engine) as session:
        expected = session.scalars(select(Journal).where(Journal.id == actual.id)).one()
        assert actual == expected


def test_retrieve_n(repo):
    entry_one_text = "Hope this doesn't show up"
    entry_two_text = "Do the thing"
    entry_three_text = "Hello world"

    entry_one = repo.create_journal_entry(entry_one_text)
    entry_two = repo.create_journal_entry(entry_two_text)
    entry_three = repo.create_journal_entry(entry_three_text)

    actual = repo.get_last_n_entries(2)
    assert len(actual) == 2
    assert entry_one not in actual
    assert entry_two in actual
    assert entry_three in actual


def test_get_today_entries(engine, repo: JournalRepo, today, yesterday):
    with Session(engine) as session:
        # Arrange
        entry_one = Journal(log="one", ts=today)
        entry_two = Journal(log="two", ts=today)
        entry_three = Journal(log="SHOULD NOT SEE", ts=yesterday)

        session.add_all([entry_one, entry_two, entry_three])
        session.commit()
        # Act
        actual = repo.get_today_entries()
        # Assert
        assert entry_one in actual
        assert entry_two in actual
        assert entry_three not in actual


def test_get_yesterday_entries(engine, repo: JournalRepo, today, yesterday):
    with Session(engine) as session:
        # Arrange
        entry_one = Journal(log="one", ts=yesterday)
        entry_two = Journal(log="two", ts=yesterday)
        entry_three = Journal(log="SHOULD NOT SEE", ts=today)

        session.add_all([entry_one, entry_two, entry_three])
        session.commit()
        # Act
        actual = repo.get_yesterday_entries()
        # Assert
        assert entry_one in actual
        assert entry_two in actual
        assert entry_three not in actual


def test_get_last_two_week_entries(engine, repo: JournalRepo, today, yesterday):
    with Session(engine) as session:
        # Arrange
        entry_one = Journal(log="one", ts=yesterday)
        entry_two = Journal(log="two", ts=yesterday)
        last_year = timedelta(days=-365)
        entry_three = Journal(log="SHOULD NOT SEE", ts=yesterday + last_year)

        session.add_all([entry_one, entry_two, entry_three])
        session.commit()
        # Act
        actual = repo.get_last_two_week_entries()
        # Assert
        assert entry_one in actual
        assert entry_two in actual
        assert entry_three not in actual
