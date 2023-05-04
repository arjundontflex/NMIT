from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from passlib.hash import pbkdf2_sha256
import os

app = Flask(__name__)
app.secret_key = 'secret-key'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission
        pass
    else:
        return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Handle form submission
        pass
    else:
        return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_folder = os.path.join(os.getcwd(), 'users', session['username'])
        files = os.listdir(user_folder)
        return render_template('dashboard.html', files=files)
    else:
        return redirect(url_for('signin'))
class SignupForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', [validators.InputRequired()])

class SigninForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired()])
    password = PasswordField('Password', validators=[validators.InputRequired()])

@app.route('/signup', methods=['GET', 'POST'])

def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = pbkdf2_sha256.hash(form.password.data)

        # Create user folder
        user_folder = os.path.join(os.getcwd(), 'users', username)
        os.makedirs(user_folder)

        # Save user data to file
        user_file = os.path.join(user_folder, 'user.txt')
        with open(user_file, 'w') as f:
            f.write(f'{username}:{password}')

        # Set session data and redirect to dashboard
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        # Check if user exists and password is correct
        user_folder = os.path.join(os.getcwd(), 'users', username)
        user_file = os.path.join(user_folder, 'user.txt')
        if os.path.exists(user_folder) and os.path.isfile(user_file):
            with open(user_file, 'r') as f:
                saved_data = f.read().strip().split(':')
                if saved_data[0] == username and pbkdf2_sha256.verify(password, saved_data[1]):
                    session['username'] = username
                    return redirect(url_for('dashboard'))

        # Authentication failed
        form.username.errors.append('Invalid username or password')

    return render_template('signin.html', form=form)

