import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.app import create_app
from server.extensions import db
from server.app.models import User, Proposal, Task, Subtask
from faker import Faker
from random import choice, randint, uniform
from datetime import datetime
from werkzeug.security import generate_password_hash

fake = Faker()

# Initialize Flask
app = create_app()
with app.app_context():
    def create_users(n=5):
        """Generate random users"""
        users = []
        for _ in range(n):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password_hash=generate_password_hash("password123"),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=choice(["user", "admin", "moderator"]),
                created_at=fake.date_time_between(start_date="-2y", end_date="now"),
                updated_at=datetime.utcnow(),
                is_active=True
            )
            db.session.add(user)
            users.append(user)
        db.session.commit()
        return users

    def create_proposals(users, n=10):
        """Generate random proposals"""
        proposals = []
        for _ in range(n):
            proposal = Proposal(
                name=fake.company(),
                site=fake.address(),
                client=fake.company(),
                status=choice(["pending", "approved", "rejected", "in_review"]),
                budget=round(uniform(1000, 100000), 2),
                deadline=fake.date_between(start_date="today", end_date="+1y"),
                description=fake.text(),
                created_at=fake.date_time_between(start_date="-1y", end_date="now"),
                updated_at=datetime.utcnow(),
                created_by=choice(users).id,
                attachments=None
            )
            db.session.add(proposal)
            proposals.append(proposal)
        db.session.commit()
        return proposals

    def create_tasks(proposals, n=20):
        """Generate random tasks"""
        tasks = []
        for _ in range(n):
            task = Task(
                proposal_id=choice(proposals).id,
                title=fake.sentence(nb_words=5),
                description=fake.text(),
                order=randint(1, 10),
                created_at=fake.date_time_between(start_date="-6m", end_date="now"),
                updated_at=datetime.utcnow(),
            )
            db.session.add(task)
            tasks.append(task)
        db.session.commit()
        return tasks

    def create_subtasks(tasks, n=50):
        """Generate random subtasks with integer hours"""
        for _ in range(n):
            subtask = Subtask(
                task_id=choice(tasks).id,
                title=fake.sentence(nb_words=4),
                hours=randint(1, 10),  # Generates only whole numbers
                order=randint(1, 5),
                created_at=fake.date_time_between(start_date="-3m", end_date="now"),
                updated_at=datetime.utcnow(),
            )
            db.session.add(subtask)
        db.session.commit()

    def generate_random_data():
        print("Generating users...")
        users = create_users(10)

        print("Generating proposals...")
        proposals = create_proposals(users, 20)

        print("Generating tasks...")
        tasks = create_tasks(proposals, 40)

        print("Generating subtasks...")
        create_subtasks(tasks, 100)

        print("Data generation complete!")

    generate_random_data()
