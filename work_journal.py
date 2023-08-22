from work_journal.core.db import ConfigRepo, JournalRepo
from work_journal.ui.main_window import MainWindow
from work_journal.core import app_config


def main():
    journal_repo = JournalRepo(app_config.db.engine)
    config_repo = ConfigRepo(app_config.db.engine)

    if "INIT" not in config_repo.config:
        config_repo.create_config(ConfigRepo.CONFIG_INIT, "True")
        config_repo.create_config(ConfigRepo.CONFIG_HISTORY_LEN, 5)
        config_repo.create_config(ConfigRepo.CONFIG_GEOMETRY, "800x220")

    app = MainWindow(journal_repo, config_repo)
    app.mainloop()


if __name__ == "__main__":
    main()
