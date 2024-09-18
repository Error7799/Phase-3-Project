import click
from models import session, User, Habit, HabitLog
from datetime import date

@click.group()
def cli():
    """Habit Tracker CLI."""
    pass

@cli.command()
@click.option('--name', prompt='User name', help='The name of the user.')
@click.option('--email', prompt='User email', help='The email of the user.')
def add_user(name, email):
    """Add a new user."""
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    click.echo(f"User '{name}' added!")

@cli.command()
@click.option('--name', prompt='Habit name', help='The name of the habit.')
@click.option('--frequency', prompt='Frequency (daily/weekly)', help='How often to complete the habit.')
@click.argument('user_id')
def add_habit(name, frequency, user_id):
    """Add a new habit."""
    habit = Habit(habit_name=name, frequency=frequency, user_id=user_id)
    session.add(habit)
    session.commit()
    click.echo(f"Habit '{name}' added for user {user_id}!")

@cli.command()
@click.argument('user_id')
def list_habits(user_id):
    """List all habits for a user."""
    habits = session.query(Habit).filter_by(user_id=user_id).all()
    if habits:
        click.echo(f"Habits for user {user_id}:")
        for habit in habits:
            click.echo(f"- {habit.habit_name} ({habit.frequency})")
    else:
        click.echo("No habits found.")

@cli.command()
@click.argument('user_id')
@click.option('--frequency', prompt='Frequency (daily/weekly)', help='Filter habits by frequency.')
def filter_habits(user_id, frequency):
    """List habits filtered by frequency."""
    habits = session.query(Habit).filter_by(user_id=user_id, frequency=frequency).all()
    if habits:
        click.echo(f"Habits with frequency '{frequency}' for user {user_id}:")
        for habit in habits:
            click.echo(f"- {habit.habit_name}")
    else:
        click.echo(f"No habits found with frequency '{frequency}'.")

@cli.command()
@click.argument('habit_id')
def complete_habit(habit_id):
    """Mark a habit as completed for today."""
    log = HabitLog(habit_id=habit_id)
    session.add(log)
    session.commit()
    click.echo(f"Habit {habit_id} marked as completed for {date.today()}!")

@cli.command()
@click.argument('habit_id')
def view_logs(habit_id):
    """View completion logs and consistency for a habit."""
    habit = session.query(Habit).get(habit_id)
    logs = session.query(HabitLog).filter_by(habit_id=habit_id).all()

    if logs:
        click.echo(f"Completion logs for habit '{habit.habit_name}':")
        for log in logs:
            click.echo(f"- Completed on {log.date_completed}")

        # Calculate consistency
        if habit.frequency == 'daily':
            expected_completions = (date.today() - logs[0].date_completed).days + 1
        elif habit.frequency == 'weekly':
            expected_completions = ((date.today() - logs[0].date_completed).days // 7) + 1
        else:
            expected_completions = len(logs)  # Default to the number of logs

        actual_completions = len(logs)
        consistency = (actual_completions / expected_completions) * 100

        click.echo(f"Consistency: {consistency:.2f}% ({actual_completions}/{expected_completions}) completions")
    else:
        click.echo(f"No logs found for habit '{habit.habit_name}'.")

@cli.command()
@click.argument('habit_id')
def delete_habit(habit_id):
    """Delete a habit."""
    habit = session.query(Habit).get(habit_id)
    if habit:
        session.delete(habit)
        session.commit()
        click.echo(f"Habit '{habit.habit_name}' deleted.")
    else:
        click.echo(f"Habit with ID {habit_id} not found.")

@cli.command()
@click.argument('habit_id')
@click.option('--name', prompt='New habit name', help='New name for the habit.')
@click.option('--frequency', prompt='New frequency (daily/weekly)', help='New frequency for the habit.')
def edit_habit(habit_id, name, frequency):
    """Edit an existing habit."""
    habit = session.query(Habit).get(habit_id)
    if habit:
        habit.habit_name = name
        habit.frequency = frequency
        session.commit()
        click.echo(f"Habit '{habit_id}' updated to '{name}' with frequency '{frequency}'.")
    else:
        click.echo(f"Habit with ID {habit_id} not found.")
