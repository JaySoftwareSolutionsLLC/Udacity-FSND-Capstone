from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Category is the highest level of this application. 1 Category = 1 Cheat Sheet
'''
class Category(db.Model):  
  __tablename__ = 'Category'

  id = Column(db.Integer, primary_key=True)
  name = Column(String(16), unique=True, nullable=False)
  description = Column(String(1024), nullable=False)
  topics = db.relationship('Topic', backref='category', lazy=True, cascade = 'all,delete-orphan')

  def __init__(self, name, description):
    self.name = name
    self.description = description

  def format(self):
    # Create a formatted topics array for display purposes
    formatted_topics = [t.format() for t in self.topics]
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'topics': formatted_topics }

'''
Topic is the middle level of this application. It belongs to a single Category. It has many Concepts that belong to it.
'''

class Topic(db.Model):
  __tablename__ = 'Topic'

  id = Column(db.Integer, primary_key=True)
  name = Column(String(16), nullable=False)
  description = Column(String(255), nullable=True)
  category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)
  concepts = db.relationship('Concept', backref='topic', lazy=True, cascade = 'all,delete-orphan')

  def __init__(self, name, description, category_id):
    self.name = name
    self.description = description
    self.category_id = category_id

  def format(self):
    formatted_concepts = [c.format() for c in self.concepts]
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'category_id': self.category_id,
      'concepts': formatted_concepts}

'''
Concept is the smallest unit of this application. It belongs to a single Topic.
'''

class Concept(db.Model):
  __tablename__ = 'Concept'

  id = Column(db.Integer, primary_key=True)
  name = Column(String(64), nullable=False)
  description = Column(String(1024), nullable=True)
  url = Column(String(128), nullable=True)
  topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)

  def __init__(self, name, description, url, topic_id):
    self.name = name
    self.description = description
    self.url = url
    self.topic_id = topic_id

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'url': self.url,
      'topic_id': self.topic_id,
      }