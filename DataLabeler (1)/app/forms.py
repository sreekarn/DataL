from wtforms import TextField, PasswordField, Form, RadioField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets.html5 import NumberInput
class RegisterForm(Form):
    first_name = TextField(
        'First Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    last_name = TextField(
        'Last Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'Institution Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    user_name = TextField(
        'User Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    institute_name = TextField(
        'Institute Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    specialization = TextField(
        'Specialization', validators=[DataRequired(), Length(min=3, max=25)]
    )
    resident_doctor = RadioField('Resident Doctor', choices=[(1, 'Yes'), (0,'No')], default=0)

    experience_years = IntegerField(widget=NumberInput(min=0),
        label = 'Years', validators=[DataRequired()], default=0
    )
    experience_months = IntegerField(widget=NumberInput(min=0),
        label = 'Months', validators=[DataRequired()], default=0
    )

    confirm = PasswordField(
        'Confirm Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    user_name = TextField('User Name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
