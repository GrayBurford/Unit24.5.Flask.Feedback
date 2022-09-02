"""Seed file to make sample data for database."""

from models import db
from app import app

# Drop all tables, if any. Then create all tables.
db.drop_all()
db.create_all()
