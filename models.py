from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    habits = relationship('Habit', back_populates='user')

class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    habit_name = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='habits')
    logs = relationship('HabitLog', back_populates='habit')

class HabitLog(Base):
    __tablename__ = 'habit_logs'
    id = Column(Integer, primary_key=True)
    date_completed = Column(Date, default=date.today)
    habit_id = Column(Integer, ForeignKey('habits.id'))
    habit = relationship('Habit', back_populates='logs')

# Database connection
engine = create_engine('sqlite:///habit_tracker.db')  # SQLite database file
Base.metadata.create_all(engine)  # Create tables based on models
Session = sessionmaker(bind=engine)  # Session factory
session = Session()  # Initialize session to interact with the database
