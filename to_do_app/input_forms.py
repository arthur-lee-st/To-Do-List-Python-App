from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class ToDoItemForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit_add = SubmitField("Add")


class EditItemForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit_edit = SubmitField("Edit")