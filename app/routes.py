from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, SignupForm, AdminLogin
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home')
def index():
    return render_template('public/home.html', title='Home')

@app.route('/explore')
def explore():
    return render_template('public/explore.html', title='About')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminLogin()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username)
        print(password)
        print(email)
    return render_template('admin/dashboard.html', title='Admin', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('loginrequired/dashboard.html', title='Dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = User.query.filter_by(username=form.username.data).first()
        if username is None or not username.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(username, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('public/Login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You Can Login Now')
        return redirect(url_for('login'))
    return render_template('public/(t)register.html', title='Register', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/500.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


