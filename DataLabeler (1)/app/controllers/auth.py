from logging import error
from flask import render_template, Blueprint, request ,redirect,jsonify,send_from_directory, url_for, current_app
from app.forms import *
from app.models import db, Project, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user, login_required
blueprint = Blueprint('auth', __name__)

@blueprint.route('/', methods=('GET', 'POST'))
@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(user_name=form.user_name.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            error = 'Please check your login details and try again.'
            return render_template('forms/login.html', form=form, error=error) # if the user doesn't exist or password is wrong, reload the page

        login_user(user, remember=True)

        existing_project = Project.query.filter(
            Project.name == "PROJECT_NAME"
        ).first()
        if existing_project:
            existing_project.username = user.user_name
            
        else:
            new_project = Project(
            name="PROJECT_NAME",
            username=user.user_name)
            db.session.add(new_project)  # Adds new Project record to database
        
        db.session.commit()  # Commits all changes

        if existing_project and existing_project.storage_location:
            return redirect('/tasks')
        
        return redirect('/add-storage')

    return render_template('forms/login.html', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    error = None
    current_app.logger.info(form.email.data)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user: # if a user is not found, we want to add it to db

            months = (form.experience_years.data * 12) + form.experience_months.data

            years = months // 12

            months = (months - years * 12)
            
            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(email=form.email.data,
                first_name=form.first_name.data,
                last_name = form.last_name.data,
                user_name = form.user_name.data,
                institute_name = form.institute_name.data,
                specialization = form.specialization.data,
                resident_doctor = int(form.resident_doctor.data),
                experience = str(years)+'.'+str(months),
                password=generate_password_hash(form.password.data, method='sha256'),
                    )

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return redirect('/')

        error = 'User already exists!'



    return render_template('forms/register.html', form=form, error=error)

@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))