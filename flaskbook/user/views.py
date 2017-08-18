from flask import Blueprint, render_template, request, redirect, session
import bcrypt
# APP MODULES
from user.models import User
from user.forms import RegisterForm, LoginForm

user_app = Blueprint('user_app', __name__)

@user_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    return render_template('user/login.html',
                            form=form,
                            error=error)
    
@user_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
            )
        user.save()
        return 'User registered'
    return render_template('user/register.html', 
                            form=form)