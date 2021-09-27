from app import db
from sqlalchemy.orm import class_mapper
from flask_login import UserMixin

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(model, c)) for c in columns)


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    user_name = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    institute_name = db.Column(db.String)
    specialization = db.Column(db.String)
    resident_doctor = db.Column(db.Boolean)
    experience = db.Column(db.String)


class Task(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    question = db.Column(db.String)
    label = db.Column(db.String)
    user_name = db.Column(db.String)
    date = db.Column(db.String)


class Project(db.Model):
    __tablename__ = 'Projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    storage_location = db.Column(db.String)
    question = db.Column(db.String)
    username = db.Column(db.String)
    last_task_id = db.Column(db.Integer)



