# Work Journal

A simple GUI for jotting down accomplishments with a timestamp and then creating reports to refresh your memory when you need them.

## Installation

This project uses `poetry` for its dependency management.  Verify that you have it installed:

```
poetry --version
```

If you do not have it installed:

```
pip install poetry
```

Best to do this from outside of any virtual environments, as this is a global utility.

1. Clone project/copy to a local directory
2. `poetry install`

## Running

```
python work_journal.py
```

## Building for Distribution

**RUN THIS FROM INSIDE YOUR VIRTUAL ENVIRONMENT!**

```
pyinstaller work_journal.spec
```

* If you do not have `pyinstaller` installed, install it using the above process for installing `poetry`.  Just sub in `pyinstaller` in place of `poetry`.
* If your virtual environment is not called `.venv`, you may need to tweak the `work_journal.spec` file at line 9:

```
pathex=['.\\.venv\\Lib\\site-packages\\'],
```

Change the path to `[venv]\Lib\site-packages` to suit your virtual environment location.

At this point, once `pyinstaller` has done its work you should have a file in a newly minted `dist` directory called `work_journal.exe`.
