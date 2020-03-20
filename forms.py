from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', widget=TextArea())
    submit = SubmitField('Submit')

class TopicForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', widget=TextArea())
    category_id = IntegerField('category_id', validators=[DataRequired()], render_kw={'disabled':''},)
    submit = SubmitField('Submit')

class ConceptForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', widget=TextArea())
    url = StringField('url')
    topic_id = IntegerField('topic_id', validators=[DataRequired()], render_kw={'disabled':''},)
    submit = SubmitField('Submit')