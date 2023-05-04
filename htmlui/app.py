import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], username))
        return redirect(url_for('dashboard'))
    else:
        return render_template('htmlui\signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in os.listdir(app.config['UPLOAD_FOLDER']):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('signin.html', error='Invalid username or password.')
    else:
        return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], session['username']))
        return render_template('dashboard.html', files=files)
    else:
        return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' in session:
        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], session['username'], filename))
                return redirect(url_for('dashboard'))
            else:
                return render_template('upload.html', error='No file selected.')
        else:
            return render_template('upload.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
