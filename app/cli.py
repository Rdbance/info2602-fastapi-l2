import typer
from sqlmodel import Session, select
from db import get_session, drop_all, create_db_and_tables
from models import User   

cli = typer.Typer()

@cli.command()
def initialize():
    """Drop all tables, recreate them, and add a default user."""
    with get_session() as db:
        drop_all()
        create_db_and_tables()
        bob = User(username="bob", email="bob@mail.com", password="bobpass")
        db.add(bob)
        db.commit()
        db.refresh(bob)
        print("Database Initialized with default user: bob")

#Task 5.1
@cli.command()
def get_user(username: str):
    """Retrieve a user by username."""
    with get_session() as db:
        statement = select(User).where(User.username == username)
        user = db.exec(statement).first()
        if user:
            print("User found:", user)
        else:
            print("User not found")

# Task 5.2
@cli.command()
def get_all_users():
    """Retrieve all users."""
    with get_session() as db:
        statement = select(User)
        users = db.exec(statement).all()
        if users:
            for u in users:
                print(u)
        else:
            print("No users in database")


# Task 6
@cli.command()
def change_email(username: str, new_email: str):
    """Update a user's email address."""
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if user:
            user.email = new_email
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Email updated:", user)
        else:
            print("User not found")


# Task 7
@cli.command()
def create_user(username: str, email: str, password: str):
    """Create a new user."""
    with get_session() as db:
        new_user = User(username=username, email=email, password=password)
        db.add(new_user)
        try:
            db.commit()
            db.refresh(new_user)
            print("User created:", new_user)
        except Exception as e:
            db.rollback()
            print("Error creating user:", e)


# Task 8: Delete a user
@cli.command()
def delete_user(username: str):
    """Delete a user by username."""
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if user:
            db.delete(user)
            db.commit()
            print("User deleted:", username)
        else:
            print("User not found")

if __name__ == "__main__":
    cli()