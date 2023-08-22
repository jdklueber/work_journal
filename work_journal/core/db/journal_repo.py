from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import Base, Journal


class JournalRepo:
    """
    Journal Repository:  This houses all code for CRUD operations on the journal table.
    """

    def __init__(self, engine) -> None:
        self.engine = engine
        Base.metadata.create_all(engine)

    def create_journal_entry(self, entry: str) -> Journal:
        """
        Create a journal entry
        entry: The string to log
        """
        with Session(bind=self.engine, expire_on_commit=False) as session:
            journal = Journal(log=entry, ts=datetime.now())
            session.add(journal)
            session.commit()
            return journal

    def get_last_n_entries(self, number_to_retrieve: int) -> [Journal]:
        """
        Retrieve last n journal entries
        number_to_retrieve: limits results to this many
        """
        with Session(self.engine) as session:
            return session.scalars(
                select(Journal).order_by(Journal.id.desc()).limit(number_to_retrieve)
            ).all()

    def _get_today_range(self) -> (datetime, datetime):
        """
        Utility method to abstract out getting the start and end of today
        Returns a tuple of datetimes (start_of_day, end_of_day):
        start_of_day = today's date, time of 00:00:00
        end_of_day = today's date, time of 23:59:59
        """
        today = datetime.now()
        today_start = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=0,
            minute=0,
            second=0,
        )

        today_end = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=23,
            minute=59,
            second=59,
        )
        return (today_start, today_end)

    def _get_yesterday_range(self):
        """
        Utility method to abstract out getting the start and end of yesterday
        Returns a tuple of datetimes (start_of_day, end_of_day):
        start_of_day = yesterday's date, time of 00:00:00
        end_of_day = yesterday's date, time of 23:59:59
        """
        (today_start, today_end) = self._get_today_range()
        delta = timedelta(days=-1)
        return (today_start + delta, today_end + delta)

    def _get_date_range_this_week(self):
        """
        Utility method to abstract out getting the start and end of the current week
        Returns a tuple of datetimes (start_of_day, end_of_day):
        start_of_day = Monday's date, time of 00:00:00
        end_of_day = Sunday's date, time of 23:59:59
        """
        (today_start, today_end) = self._get_today_range()
        delta_to_start_of_week = timedelta(days=(-1 * today_start.weekday()))
        delta_to_end_of_week = timedelta(days=6 - today_start.weekday())
        start_of_week = today_start + delta_to_start_of_week
        end_of_week = today_end + delta_to_end_of_week
        return (start_of_week, end_of_week)

    def get_entries_for_range(self, start, end):
        """
        Given two datetime objects, return all Journal entries falling in that range
        start:  datetime, start of range
        end: datetime, end of range
        """

        with Session(self.engine) as session:
            return session.scalars(
                select(Journal).where(Journal.ts.between(start, end))
            ).all()

    def get_today_entries(self) -> [Journal]:
        """
        Uses get_entries_for_range to return all Journal entries with today's date
        """
        (start, end) = self._get_today_range()
        return self.get_entries_for_range(start, end)

    def get_yesterday_entries(self) -> [Journal]:
        """
        Uses get_entries_for_range to return all Journal entries with yesterday's date
        """
        (start, end) = self._get_yesterday_range()
        print(start)
        print(end)
        return self.get_entries_for_range(start, end)

    def get_last_two_week_entries(self) -> [Journal]:
        """
        Uses get_entries_for_range to return all Journal entries for the prior two weeks
        """
        (start_of_week, end_of_period) = self._get_date_range_this_week()
        start_of_period = start_of_week + timedelta(days=-7)
        return self.get_entries_for_range(start_of_period, end_of_period)
