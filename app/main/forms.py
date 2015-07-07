from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Interestedpeople


class NamePhoneForm(Form):
    name = StringField('your name', validators=[Required()])
    phone = StringField('phone number', validators=[Required()])
    submit = SubmitField('Submit')
