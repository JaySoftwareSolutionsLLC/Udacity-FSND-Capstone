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
Person
Have title and release year
'''
class Category(db.Model):  
  __tablename__ = 'Category'

  id = Column(db.Integer, primary_key=True)
  name = Column(String(16))
  description = Column(String(1024))

  def __init__(self, name, description):
    self.name = name
    self.description = description

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description}