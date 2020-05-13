from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
from html import escape

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
    topics = db.relationship('Topic',
                             backref='category',
                             lazy=True,
                             cascade='all,delete-orphan')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def html_format(self):
        op = """<a href='/categories/{0}' class='category' data-id='{0}'>
                    <h2>{1}</h2>
                    <p>{2}</p>
                    <i class='fas fa-pencil-alt upper-left' title='Edit {1}' data-model='category' data-id='{0}'></i>
                </a>""".format(self.id, self.name, self.description)    
        return op

    def format(self):
        # Create a formatted topics array for display purposes
        formatted_topics = [t.format() for t in self.topics]
        html = self.html_format()
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'topics': formatted_topics,
            'html': html}


'''
Topic is the middle level of this application.
It belongs to a single Category.
It has many Concepts that belong to it.
'''


class Topic(db.Model):
    __tablename__ = 'Topic'

    id = Column(db.Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    description = Column(String(255), nullable=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('Category.id'),
                            nullable=False)
    concepts = db.relationship('Concept',
                               backref='topic',
                               lazy=True,
                               cascade='all,delete-orphan')

    def __init__(self, name, description, category_id):
        self.name = name
        self.description = description
        self.category_id = category_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def html_format(self):
        concepts_str = ""
        for c in self.concepts:
            concepts_str += c.html_format()
        op = """<ul class='topic' data-id='{0}'>
                    <i class="fas fa-plus" data-model="concept" data-parent-id='{0}' title="New {1} Concept"></i>
                    <h2>{1}<i class='fas fa-pencil-alt' data-model="topic" data-id='{0}' title="Edit '{1}'"></i></h2>
                    <p>{2}</p>
                    {3}
                </ul>""".format(self.id, self.name, self.description, concepts_str)    
        return op

    def format(self):
        formatted_concepts = [c.format() for c in self.concepts]
        html = self.html_format()
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'concepts': formatted_concepts,
            'html': html}


'''
Concept is the smallest unit of this application. It belongs to a single Topic.
'''


class Concept(db.Model):
    __tablename__ = 'Concept'

    id = Column(db.Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    url = Column(String(128), nullable=True)
    topic_id = db.Column(db.Integer,
                         db.ForeignKey('Topic.id'),
                         nullable=False)
    tags = db.relationship('ConceptTag', backref='concept', lazy=True, cascade = 'delete-orphan')

    def __init__(self, name, description, url, topic_id):
        self.name = name
        self.description = description
        self.url = url
        self.topic_id = topic_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def html_format(self):
        url_str = ""
        if (self.url):
            url_str = """<a href='{0}' target='_blank' title='visit website'>
                            <i class='fas fa-rocket'></i>
                         </a>""".format(self.url)
        op = """<li class='concept' data-id='{0}'>
                    {2}
                    <a href='#'  title='Click to Copy' data-clipboard-text='{1}'
                    class='copy-to-clipboard' >{1}</a>
                    <i class='fas fa-pencil-alt' data-model='concept'
                    data-id='{0}' title="Edit '{1}'"></i>
        </li>""".format(self.id, escape(self.name), url_str)
        return op

    def format(self):
        html = self.html_format()
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'topic_id': self.topic_id,
            'html': html
        }

# Tags are ways to categorize content
class Tag(db.Model):
    __tablename__ = 'Tag'
    id = Column(db.Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    description = Column(String(256), nullable=True)
    concepts = db.relationship('ConceptTag', backref='tag', lazy=True, cascade = 'delete-orphan')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        html = self.html_format()
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

# association table between Tag and Concept
class ConceptTag(db.Model):
    __tablename__ = 'ConceptTag'

    concept_id = db.Column(db.ForeignKey('Concept.id'), primary_key = True)
    tag_id = db.Column(db.ForeignKey('Tag.id'), primary_key = True)