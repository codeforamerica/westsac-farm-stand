from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, SubmitField, RadioField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Interestedpeople, Role, User, Product


class NamePhoneForm(Form):
    name = StringField('your name', validators=[Required()])
    phone = StringField('phone number', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    farm_name = StringField('Name of your farm', validators=[Length(0,64)])
    url = StringField('Your website', validators=[Length(0,64)])
    submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    url = StringField('Your website', validators=[Length(0,64)])
    farm_name = StringField('Name of your farm', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class ProductForm(Form):
    name = StringField('Crop Name', validators=[Length(0, 64)])
    status = SelectField('Status', choices=[('1','Available'),('2','Unavailable'),('3','Hidden')])
    price = StringField('Price')
    starts = StringField('Available From')
    ends = StringField('To')
    submit = SubmitField('Submit')
