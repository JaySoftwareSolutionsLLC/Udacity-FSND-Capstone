from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class CategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', widget=TextArea())
    submit = SubmitField('Submit')