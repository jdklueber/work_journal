"""
This module encapsulates the database connectivity for the rest of the application.
This is to abstract the engine creation logic away from the configuration logic.
This might turn out to be overkill, but I'd rather start this way than have to 
unsnarl it later...
"""
from sqlalchemy import create_engine


class DBManager:
    """
    Manages a singleton SQLAlchemy Engine instance
    """

    def __init__(self, db_url: str) -> None:
        """
        db_url: SQLAlchemy database URL
        For details see: https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
        """
        self.engine = create_engine(db_url)
