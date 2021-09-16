from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from jobby.models import Users, Notification
from datetime import datetime
from jobby import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from utils import send_confirmation_email

account = Blueprint('account',__name__)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        login_eu = request.form['login_eu']
        password = request.form['password']

        if "@" in login_eu:
            user = Users.query.filter_by(email=login_eu).first()
        else:
            user = Users.query.filter_by(username=login_eu).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('manage.dashboard'))
            else:
                flash('Wrong Credentials! Check your spelling.')
                return render_template('account/login.html')
        else:
            flash('Wrong Credentials! Check your spelling.')
            return render_template('account/login.html')
    return render_template('account/login.html')

@account.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Passwords not matched! Try again')
            return render_template('account/signup.html')
        if not username.isalnum():
            flash('username should be alpha numeric!')
            return render_template('account/signup.html')

        hashed_password = generate_password_hash(password, method='sha256')
        existing_username = Users.query.filter_by(username=username).first()
        if existing_username is not None:
            flash('Username already being used!')
            return render_template('account/signup.html')
        else:
            existing_email = Users.query.filter_by(email=email).first()
            if existing_email is not None:
                flash('Email already being used')
                return render_template('account/signup.html')
            else:
                new_user = Users(username=username, email=email, password=hashed_password,
                    member_since=datetime.utcnow(), status='employer', email_approved=True)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return render_template('account/welcome.html')
    return render_template('account/signup.html')

@account.route('/confirm_email/<token>')
def confirm_email(token):
    user = Users.verify_confirmation_token(token)
    if not user:
        abort(404)
    notif = Notification.query.filter_by(notification_to=current_user, not_type=2).first_or_404()
    db.session.delete(notif)
    user.email_approved = True
    db.session.commit()
    flash('Your email address has been confirmed!')
    return render_template('dashboard/dashboard.html')


@account.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
