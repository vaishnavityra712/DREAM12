from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from . import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from website import create_app
from flask_mail import Message


auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer('trivialthing')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first_or_404()
        if user:
                if check_password_hash(user.password, password):
                    flash(f'Hello {user.first_name}!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # token = s.dumps(email, salt='email-confirm')
            new_user = User(email=email, first_name=first_name, confirmed=True, password=generate_password_hash(
                password1, method='sha256'))

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            # msg = Message('Confirm Email', sender='magaa600@gmail.com', recipients=[email])
            # confirm_url = url_for('auth.activate', token=token, _external=True)
            # msg.body = 'Follow the link in order to confirm your email'
            # msg.html = render_template('activate.html',confirm_url=confirm_url)
            # mail.send(msg)                        

    return render_template("sign_up.html", user=current_user)


@auth.route('/activate/<token>')

def activate(token):
    
    email = s.loads(token, salt='email-confirm', max_age=3600)

    user = User.query.filter_by(email=email).first_or_404()

    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for("views.home", user=current_user))
    