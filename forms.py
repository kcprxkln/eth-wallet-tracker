from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=24)])
    password = StringField('Password', validators=[DataRequired(), Length(min=4, max=24)])
    submit = SubmitField('Log in')

    
class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=24)])
    password = StringField('Password', validators=[DataRequired(), Length(min=4, max=24)])
    submit = SubmitField('Register')