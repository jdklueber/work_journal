# Database Design - Work Journal Application

The database for this application will be incredibly simple, as it is a single user application that tracks exactly one thing.  This will be implemented in SQLite for maximum simplicity, but because I will be using SQLAlchemy and Alembic to manage everything, it should be portable to a Real Database(tm) with little effort.

## Table:  Journal

This is the meat of the application.  Simple table, just a primary key, a timestamp, and a log message.

| Column | Type      | Purpose                     |
| ------ | --------- | --------------------------- |
| id     | numeric   | Primary key                 |
| ts     | timestamp | Timestamp for the log entry |
| log    | string    | The message being logged    |



## Table:  Config

I might or might not need this, but I want to have the option to configure the application to suit myself.  If I don't need it, I won't actually implement it, but this is what it will look like if I do.

| Column | Type    | Purpose                             |
| ------ | ------- | ----------------------------------- |
| id     | numeric | Primary key                         |
| key    | string  | Configuration key                   |
| value  | string  | The value of the element configured |

