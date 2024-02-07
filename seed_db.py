from app import app
from database.db import db
from model.detector import Detector
from model.organization import Organization
from model.rule import Rules
import glob
import update_db


def seed_db():
    with app.app_context():
        db.create_all()

        # Create Some organizations
        organizations = [
            Organization(name='Hunters', is_blacklist=True),
            Organization(name='Google', is_blacklist=False),
            Organization(name='Databricks', is_blacklist=True),
            Organization(name='Amazon', is_blacklist=False)
        ]

        for org in organizations:
            db.session.add(org)


        db.session.commit()
        yamls = glob.glob("./detectors/*.yaml") 
        for yam in yamls:       
            update_db.update_db(" ", yam)


if __name__ == "__main__":
    seed_db()
