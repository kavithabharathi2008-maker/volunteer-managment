from app import app, db
from models import User, Issue, Volunteer, Task
from utils.matching import calculate_priority_score
from datetime import datetime

def seed():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("Seeding database...")

        # 1. Create Users
        users = [
            User(name="Admin User", email="admin@example.com", role="Admin", password_hash="admin123"),
            User(name="City NGO", email="ngo@example.com", role="NGO", location="San Francisco"),
            User(name="John Doe", email="john@example.com", role="Volunteer", location="San Francisco"),
            User(name="Jane Smith", email="jane@example.com", role="Volunteer", location="Oakland"),
            User(name="Bob Helper", email="bob@example.com", role="Volunteer", location="San Francisco"),
        ]
        for u in users:
            db.session.add(u)
        db.session.commit()

        # 2. Create Volunteers
        volunteers = [
            Volunteer(user_id=users[2].id, name="John Doe", skills="medical, first aid, nursing", availability="Immediate", location="San Francisco"),
            Volunteer(user_id=users[3].id, name="Jane Smith", skills="teaching, education, tutoring", availability="Weekends", location="Oakland"),
            Volunteer(user_id=users[4].id, name="Bob Helper", skills="driving, delivery, logistics", availability="Flexible", location="San Francisco"),
        ]
        for v in volunteers:
            db.session.add(v)
        db.session.commit()

        # 3. Create Issues
        issues = [
            Issue(location="Mission District", category="Health", urgency=5, description="Urgent need for first aid supplies and medical assistance at community center.", latitude=37.7599, longitude=-122.4148, reported_by_id=users[1].id),
            Issue(location="Tenderloin", category="Food", urgency=4, description="Food bank running low on supplies. Need delivery drivers for distribution.", latitude=37.7847, longitude=-122.4145, reported_by_id=users[1].id),
            Issue(location="Oakland", category="Education", urgency=3, description="Local school needs volunteer tutors for after-school programs.", latitude=37.8044, longitude=-122.2711, reported_by_id=users[1].id),
            Issue(location="SoMa", category="Environment", urgency=2, description="Park cleanup initiative scheduled for next month. Need volunteers for coordination.", latitude=37.7785, longitude=-122.3956, reported_by_id=users[1].id),
        ]
        for i in issues:
            db.session.add(i)
            db.session.flush()
            # Create Task for each issue
            task = Task(issue_id=i.id, priority_score=calculate_priority_score(i))
            db.session.add(task)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
