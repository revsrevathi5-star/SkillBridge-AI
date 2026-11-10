from app import app
from extensions import db
from models import User, Resume, Job, SkillMatch

with app.app_context():
    db.create_all()

    print("Database created successfully!")

    for table in db.metadata.sorted_tables:
        print("Table:", table.name)