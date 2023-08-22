from . import Config
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import Config


class ConfigRepo:
    """
    Config Repository:  This houses all code for CRUD operations on the config table.
    This repo stores key/value pairs in the database and also caches them in memory for
    efficient access at runtime.  The number of key/value pairs in the database should be
    minimal, so this caching will limit round trips to the database without affecting the
    memory footprint too much.
    """

    CONFIG_INIT = "INIT"
    CONFIG_HISTORY_LEN = "HISTORY_LEN"
    CONFIG_GEOMETRY = "GEOMETRY"

    def __init__(self, engine) -> None:
        self.engine = engine
        self.config = dict()
        for config in self.retrieve_all():
            self.config[config.key] = config.value

    def create_config(self, key: str, value: str) -> Config:
        """
        Create and save a Config object
        key and value are strings, and do exactly what you think.
        """
        result = Config(key=key, value=value)
        with Session(bind=self.engine, expire_on_commit=False) as session:
            session.add(result)
            session.commit()
        self.config[key] = value
        return result

    def retrieve_all(self) -> [Config]:
        """
        Retrieves all Config objects from database
        """
        with Session(self.engine) as session:
            return session.scalars(select(Config)).all()

    def retrieve_by_key(self, key: str):
        """
        Retrieve a single Config record by key
        """
        with Session(self.engine) as session:
            return session.scalar(select(Config).filter(Config.key == key))

    def update(self, key: str, value: str) -> Config:
        """
        Update a single Config record by key
        """
        config = self.retrieve_by_key(key)
        if config:
            config.value = value
            with Session(bind=self.engine, expire_on_commit=False) as session:
                session.add(config)
                session.commit()
                return config
        else:
            raise KeyError(f"{key} not found.")

    def delete(self, key: str) -> Config:
        """
        Delete a single Config record by key
        """
        config = self.retrieve_by_key(key)
        if config:
            with Session(bind=self.engine, expire_on_commit=False) as session:
                session.delete(config)
                session.commit()
                return config
        else:
            raise KeyError(f"{key} not found.")
