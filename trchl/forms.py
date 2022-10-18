
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (BooleanField, DateField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from trchl.models import User


class FormRegister(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 25)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    passwd = PasswordField('Password', validators=[Length(6, 30)])
    passwdck = PasswordField('Password confirmation', validators=[EqualTo('passwd')])
    submit_register_button = SubmitField('Create Account')

    def validate_email(self, email):
        same_email = User.query.filter_by(email=email.data).first()
        if same_email:
            raise ValidationError('E-mail already registered. Log in, or try to sign up using another e-mail.')
    
    def validate_username(self, username):
        same_username = User.query.filter_by(username=username.data).first()
        if same_username:
            raise ValidationError('Username already taken. Please choose a different username.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    passwd = PasswordField('Password', validators=[Length(6, 30)])
    remember_session = BooleanField('Remember me')
    submit_login_button = SubmitField('Log in')


class FormNewPost(FlaskForm):
    title = StringField('Post title:', render_kw={"placeholder": "up to 60 characters..."}, validators=[DataRequired(), Length(2,60)])
    body = TextAreaField('Body:', render_kw={"placeholder": "write up to 5000 characters here...", "rows": 5}, validators=[DataRequired(), Length(3,5000)])
    submit_button = SubmitField('Create')
    save_edits_button = SubmitField('Save Edits')
    testarea = TextAreaField()


class FormEditProfile(FlaskForm):
    fullname = StringField('Full name', validators=[Length(0, 50)])
    username = StringField('Username', validators=[DataRequired(), Length(3, 25)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    place = StringField('Place', validators=[Length(0, 50)])
    profile_pic = FileField('Change Profile Picture', [FileAllowed(['jpg', 'jpeg', 'png'], 'JPG, JPEG or PNG only!')], description='potatoooooooooo')
    remove_pic = SelectField('', choices=['', "I don't want a picture"])
    tech_python = BooleanField('Python')
    tech_java = BooleanField('Java')
    tech_javascript = BooleanField('Javascript')
    tech_node = BooleanField('Node.js')
    tech_cplus = BooleanField('C/C#/C++')
    tech_sql = BooleanField('SQL')
    tech_ruby = BooleanField('Ruby')
    tech_swift = BooleanField('Swift')
    tech_rust = BooleanField('Rust')
    tech_other = BooleanField('Other')
    submit_edit_button = SubmitField('Apply changes')

    def validate_new_email(self, email):
        # verificando se ele alterou o email ou não
        if current_user.email != email.data:
            email_exists = User.query.filter_by(email=email.data).first()
            if email_exists:
                raise ValidationError('E-mail already registered. Please choose another e-mail.')

    def validate_new_username(self, username):
        # verificando se ele alterou o email ou não
        if current_user.username != username.data:
            user_exists = User.query.filter_by(email=username.data).first()
            if user_exists:
                raise ValidationError('Username already taken. Please choose a different one.')


