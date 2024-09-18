# Habit Tracker

A simple CLI application to track habits using SQLAlchemy and Click. You can create habits, mark them as completed, view logs, filter habits by frequency, and edit or delete them.

##### Features
 - Add users and habits.
 - Track habit completions with logs.
 - Filter habits by frequency (daily/weekly).
 - View habit logs to see how consistent the user has been.
 - Edit or delete habits.

# Setup

#### Install dependencies using Pipenv:
 - pipenv install

#### Activate the virtual environment:
 - pipenv shell

#### Initialize the database:
 - python app.py

# Usage

#### Add a user:
 - python app.py add-user

#### Add a habit for a user:
To add a new habit for an existing user (you’ll need the user_id)
 - python app.py add-habit --name "Exercise" --frequency "daily" 1

 - This will create a new habit called "Exercise" with a daily frequency for the user with user_id = 1.

#### List habits for a user:
 - python app.py list-habits 1

#### Filter habits by frequency:
 - python app.py filter-habits 1 --frequency "daily" (or "weekly")

#### Mark a habit as complete:
 - python app.py complete-habit 1

#### View logs and consistency for a habit:
 - python app.py view-logs 1

#### Edit a habit:
 - python app.py edit-habit 1 --name "Morning Run" --frequency "weekly"

#### Delete a habit:
 - python app.py delete-habit 1





