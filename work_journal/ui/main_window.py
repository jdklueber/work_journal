import tkinter as tk
import tkinter.ttk as ttk

from work_journal.core.db import JournalRepo, ConfigRepo
from .reports_window import ReportsWindow

STICKY_X = [tk.W, tk.E]
STICKY_ALL = [tk.W, tk.N, tk.E, tk.S]


class MainWindow(tk.Tk):
    """
    Application main window
    """

    def __init__(self, journal_repo: JournalRepo, config_repo: ConfigRepo) -> None:
        """
        journal_repo:  The configured journal table repo for this app
        config_repo:  The configured config table repo for this app
        """
        super().__init__()
        self.geometry(config_repo.config[ConfigRepo.CONFIG_GEOMETRY])
        self.title("Work Journal")
        self.resizable(False, False)
        self.repo = journal_repo
        self.config_repo = config_repo

        self.master_frame = ttk.Frame(padding=(20, 20))

        self.history_frame = JournalHistoryFrame(
            root=self.master_frame,
            repo=self.repo,
            history_length=config_repo.config[ConfigRepo.CONFIG_HISTORY_LEN],
        )
        self.history_frame.grid(row=1, column=0, sticky=STICKY_X)

        JournalEntryFrame(self.master_frame, self.repo, self.refresh_view).grid(
            row=0, column=0, sticky=STICKY_X
        )
        self.columnconfigure(0, weight=1)
        ttk.Button(self.master_frame, text="Reports", command=self.load_reports).grid(
            row=2, column=0, sticky=tk.E, pady=10
        )
        self.master_frame.columnconfigure(0, weight=1)
        self.master_frame.grid(sticky=STICKY_ALL)

        self.can_open_reports = True

        self.refresh_view()

    def refresh_view(self):
        """
        Called when the history window needs to be refreshed.  Passed as a callback into the
        journal entry frame.
        """
        self.history_frame.refresh_view()

    def load_reports(self):
        """
        Handles the button which loads the report window
        """
        if self.can_open_reports:
            ReportsWindow(
                deregister_callback=self.close_reports_callback,
                repo=self.repo,
                config_repo=self.config_repo,
                parent_geometry=self.geometry(),
            )
            self.can_open_reports = False

    def close_reports_callback(self):
        """
        Passed into the reports window.  Unlocks the reports button for further use.
        """
        self.can_open_reports = True


class JournalEntryFrame(ttk.Frame):
    """
    This Frame contains the journal entry input field.
    """

    def __init__(self, root, repo: JournalRepo, refresh_callback: callable) -> None:
        """
        root:  The parent container
        repo:  The journal table repo configured for this app.
        refresh_callback:  Called to indicate that the journal table has been updated
        """
        super().__init__(root, padding=(0, 10))
        self.repo = repo
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="Journal Entry: ").grid(row=0, column=0)
        self.journal_entry = tk.StringVar("")
        self.input = ttk.Entry(self, textvariable=self.journal_entry)
        self.input.grid(row=0, column=1, sticky=STICKY_X)
        self.input.bind("<Return>", self.save_journal)
        self.refresh_callback = refresh_callback

    def save_journal(self, _):
        """
        Stores the journal enty, clears the input field, and calls for a history refresh
        """
        self.repo.create_journal_entry(self.journal_entry.get())
        self.journal_entry.set("")
        self.refresh_callback()


class JournalHistoryFrame(ttk.Frame):
    """
    This frame displays the most recent N journal entries
    """

    def __init__(self, root, repo: JournalRepo, history_length: int):
        """
        root:  The parent container
        repo:  The journal table repo configured for this app
        history_length:  How many journal entries to display
        """
        super().__init__(root, padding=(10, 10), relief="groove", borderwidth=1)
        self.repo = repo
        self.history_length = history_length
        self.history = tk.StringVar()
        self.display_label = ttk.Label(self, textvariable=self.history)
        self.columnconfigure(0, weight=1)
        self.display_label.grid(row=0, column=0, sticky=STICKY_ALL)
        self.refresh_view()

    def refresh_view(self):
        """
        Refreshes the most recent journal entries
        """
        history = self.repo.get_last_n_entries(self.history_length)
        result = ""
        for entry in history:
            result += f"{entry.ts.strftime('%Y-%m-%d %H:%M'):<15}: {entry.log}\n"

        self.history.set(result)
