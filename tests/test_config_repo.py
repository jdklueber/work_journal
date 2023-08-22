import pytest
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from work_journal.core.db import ConfigRepo, Config
from .test_db import get_clean_db


@pytest.fixture
def engine():
    return get_clean_db()


@pytest.fixture
def repo(engine) -> ConfigRepo:
    return ConfigRepo(engine)


@pytest.fixture
def test_data(repo: ConfigRepo) -> [Config]:
    test_data = []

    test_data.append(repo.create_config("key1", "value1"))
    test_data.append(repo.create_config("key2", "value2"))
    test_data.append(repo.create_config("key3", "value3"))

    return test_data


def test_create(engine, repo):
    actual = repo.create_config("new key", "value of key")

    with Session(engine) as session:
        expected = session.scalars(select(Config).where(Config.id == actual.id)).one()
        # Verify retrieval matches insert
        assert actual == expected

        # Newly created records should be in the repo.config dictionary
        assert actual.key in repo.config
        assert repo.config[actual.key] == actual.value


def test_load(test_data: [Config], engine):
    # Verify that all config entries that pre-existed the Repo instance are loaded
    # into the config.repo dict
    repo = ConfigRepo(engine)
    for element in test_data:
        assert element.key in repo.config
        assert repo.config[element.key] == element.value


def test_retrieve_by_key(repo: ConfigRepo, engine, test_data):
    expected = test_data[0]
    assert repo.retrieve_by_key(expected.key) == expected


def test_update_404(repo):
    # Should raise a KeyError if the key doesn't exist
    try:
        repo.update("notakey", "newvalue")
        assert False
    except KeyError:
        assert True


def test_update_success(repo: ConfigRepo, test_data):
    expected = test_data[0]
    expected.value = "Hope This Works"

    try:
        repo.update(expected.key, expected.value)
        actual = repo.retrieve_by_key(expected.key)
        assert actual == expected
    except KeyError:
        assert False


def test_delete_404(repo):
    # Should raise a KeyError if the key doesn't exist
    try:
        repo.delete("notakey")
        assert False
    except KeyError:
        assert True


def test_delete_success(repo: ConfigRepo, test_data):
    try:
        expected = test_data[0]
        repo.delete(expected.key)
    except KeyError:
        assert False

    actual = repo.retrieve_by_key(expected.key)
    assert actual is None
