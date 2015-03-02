import collections.abc
import os
import pathlib

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.login import (LoginManager, login_required, login_user,
                             logout_user)
from flask.ext.mail import Mail, Message
from flask_wtf.csrf import CsrfProtect

from alps import ayah
from alps.config import read_config
from alps.db import session, setup_session
from alps.forms import login_error_msg, SignInForm, SignUpForm
from alps.model import import_all_modules
from alps.user import User


__all__ = 'app', 'initialize_app', 'login_manager'

import_all_modules()

app = Flask(__name__, template_folder='templates')
setup_session(app)
login_manager = LoginManager()
csrf_protect = CsrfProtect()
mail = Mail()

login_manager.init_app(app)
login_manager.login_view = 'login'
csrf_protect.init_app(app)
mail.init_app(app)

# import logging, sys
# logging.basicConfig(stream=sys.stderr)


def initialize_app(app=None, config_dict=None):
    if app is None:
        raise ValueError('argument app is missing or None')
    if config_dict is None:
        raise ValueError('argument config_dict is missing or None')
    if not isinstance(config_dict, collections.abc.Mapping):
        raise ValueError('argument config_dict is not a dictionary type')

    app.config.update(config_dict)

    # Make Game Style Embedded.
    # Add your Publisher Key and Scoring Key to Config File.
    ayah.configure(app.config['AYAH_PUBLISHER_KEY'],
                   app.config['AYAH_SCORING_KEY'])


try:
    env_config = os.environ['ALPS_CONFIG']
    config_dict = read_config(pathlib.Path(os.environ['ALPS_CONFIG']))
    initialize_app(app, config_dict)
except KeyError:
    pass


@login_manager.user_loader
def load_user(username):
    return session.query(User).filter_by(username=username).first()


@app.route('/')
def index():
    return render_template('index.html', msg='Hello, ALPS!')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form,
                                   err_msg=login_error_msg)
        else:
            login_user(load_user(form.username.data))
            return redirect(request.form.get('next') or url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html', form=form,
                               err_msg=login_error_msg,
                               next=request.args.get('next'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm()
    use_ayah = app.config['USE_AYAH']

    if request.method == 'POST':
        if use_ayah:
            ayah_passed = ayah.score_result(request.form['session_secret'])
        else:
            ayah_passed = None

        if not form.validate() or (use_ayah and not ayah_passed):
            if (use_ayah and not ayah_passed):
                form.errors.update({'ayah': ['AYAH test failed']})

            if use_ayah:
                return render_template('register.html', form=form,
                                       ayah=ayah.get_publisher_html())
            else:
                return render_template('register.html', form=form)
        else:
            # TODO: insert the user in DB
            # TODO: show message for new user
            return redirect(url_for('index'))
    elif request.method == 'GET':
        if use_ayah:
            return render_template('register.html', form=form,
                                   ayah=ayah.get_publisher_html())
        else:
            return render_template('register.html', form=form)


@app.route('/test_mail')
def test_mail():
    msg = Message('Hello',
                  body='Hello, World!',
                  recipients=["test@example.com"])
    msg.sender = app.config['DEFAULT_MAIL_SENDER']
    mail.send(msg)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('index'))
