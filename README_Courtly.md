# Courtly

## Requirements

-   Python 3.12+
-   Git

## Setup

### 1. Clone the repository

``` powershell
git clone <REPOSITORY_URL>
cd <REPOSITORY_FOLDER>
```

If you already have the project, update it instead:

``` powershell
git pull
```

### 2. Create and activate a virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once:

``` powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again.

### 3. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create the database

``` powershell
python manage.py migrate
```

This creates the local database tables using the project's migrations.

### 5. Create an admin account

``` powershell
python manage.py createsuperuser
```

Each team member should create their own local admin account.

### 6. Run the development server

``` powershell
python manage.py runserver
```

Open these addresses in your browser:

-   Application: http://127.0.0.1:8000/
-   Django Admin: http://127.0.0.1:8000/admin/

Stop the server with `Ctrl + C`.

## Notes

-   Each team member must create their own `.venv`.
-   The `.venv` folder is not shared through Git.
-   The local SQLite database (`db.sqlite3`) is not shared through Git.
-   Each team member has their own local database and admin account.
-   After pulling new code, install any newly added dependencies and run
    migrations if needed:

``` powershell
pip install -r requirements.txt
python manage.py migrate
```
