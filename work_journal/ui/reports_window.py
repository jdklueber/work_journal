from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, filedialog
from work_journal.core.db import Journal, JournalRepo, ConfigRepo

TF_RADIO_TODAY = "today"
TF_RADIO_YESTERDAY = "yesterday"
TF_RADIO_LASTTWO = "last_two"
TF_RADIO_LAST_YEAR = "year"

EXPORT_CSV = "csv"
EXPORT_MARKDOWN = "md"

STICKY_ALL = [tk.W, tk.N, tk.E, tk.S]


class ReportsWindow(tk.Toplevel):
    """
    This window is used to export data from the database.
    deregister_callback:  callable.  Allows the parent window to react to this one being closed
    repo:  The journal table repo
    config_repo:  The config table repo.  Currently not used by this window but just in case
    parent_geometry:  Passed in as a string so that this window matches its parent.
    """

    def __init__(
        self,
        deregister_callback: callable,
        repo: JournalRepo,
        config_repo: ConfigRepo,
        parent_geometry: str,
    ) -> None:
        super().__init__()
        self.repo = repo
        self.config_repo = config_repo
        self.title("Work Journal: Reports")
        self.kill = self.create_deregister_callback(deregister_callback)
        self.protocol("WM_DELETE_WINDOW", self.kill)
        self.geometry(parent_geometry)
        self.resizable(False, False)

        # Form Variables
        self.timeframe = tk.StringVar(value=TF_RADIO_TODAY)
        self.report_format = tk.StringVar(value=EXPORT_CSV)

        # Top Frame:  Report timeframe selector
        top_frame = ttk.Frame(self, padding=(10, 10), relief="groove", borderwidth=1)
        ttk.Radiobutton(
            top_frame, text="Today", variable=self.timeframe, value=TF_RADIO_TODAY
        ).grid(sticky=tk.W)
        ttk.Radiobutton(
            top_frame,
            text="Yesterday",
            variable=self.timeframe,
            value=TF_RADIO_YESTERDAY,
        ).grid(sticky=tk.W)
        ttk.Radiobutton(
            top_frame,
            text="Last Two Weeks",
            variable=self.timeframe,
            value=TF_RADIO_LASTTWO,
        ).grid(sticky=tk.W)
        ttk.Radiobutton(
            top_frame,
            text="Full Year",
            variable=self.timeframe,
            value=TF_RADIO_LAST_YEAR,
        ).grid(sticky=tk.W)
        top_frame.grid(column=0, row=0, sticky=STICKY_ALL, padx=10, pady=10)

        # Bottom frame:  File format and export button
        bottom_frame = ttk.Frame(self, padding=(10, 10), relief="groove", borderwidth=1)
        ttk.Radiobutton(
            bottom_frame, text="CSV", variable=self.report_format, value=EXPORT_CSV
        ).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(
            bottom_frame,
            text="Markdown",
            variable=self.report_format,
            value=EXPORT_MARKDOWN,
        ).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(bottom_frame, text="Export", command=self.perform_export).grid(
            row=0, column=2, sticky=tk.E
        )
        bottom_frame.grid(column=0, row=1, sticky=STICKY_ALL, padx=10, pady=10)
        self.columnconfigure(0, weight=1)

    def perform_export(self):
        """
        Takes the current configured export and runs it.
        """
        timeframe = self.timeframe.get()
        file_format = self.report_format.get()
        filename = filedialog.asksaveasfilename(defaultextension=file_format)

        data = []
        if timeframe == TF_RADIO_TODAY:
            data = self.repo.get_today_entries()
        elif timeframe == TF_RADIO_YESTERDAY:
            data = self.repo.get_yesterday_entries()
        elif timeframe == TF_RADIO_LASTTWO:
            data = self.repo.get_last_two_week_entries
        elif timeframe == TF_RADIO_LAST_YEAR:
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
            start_time = today_start + timedelta(days=-365)
            end_time = today_end
            data = self.repo.get_entries_for_range(start_time, end_time)

        if file_format == EXPORT_CSV:
            self.export_csv(filename, data)
        elif file_format == EXPORT_MARKDOWN:
            self.export_md(filename, data)

        self.kill()

    def export_csv(self, filename, data: [Journal]):
        """
        Handles the CSV export logic.  A candidate to be broken out into a separate module.
        filename:  path to the file to export to
        data:  a list of Journal objects to be exported.
        """
        with open(filename, "w") as fh:
            fh.write("timestamp,log_entry\n")
            for entry in data:
                fh.write(f"{entry.ts},{entry.log}\n")

    def export_md(self, filename, data: [Journal]):
        """
        Handles the markdown export logic.  A candidate to be broken out into a separate module.
        filename:  path to the file to export to
        data:  a list of Journal objects to be exported.
        """
        with open(filename, "w") as fh:
            fh.write("# Journal Entries\n")
            fh.write("| Timestamp | Log Entry |\n")
            for entry in data:
                fh.write(f"|{entry.ts}|{entry.log}|\n")

    def create_deregister_callback(self, callback: callable):
        """
        This closure creates a callback that can be used to notify the creating
        window that this one is closing and then procedes to close.
        """

        def new_callback():
            callback()
            self.destroy()

        return new_callback
