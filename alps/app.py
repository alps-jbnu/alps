import collections.abc
import os
import pathlib

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.login import (LoginManager, login_required, login_user,
                             logout_user)
from flask_wtf.csrf import CsrfProtect
from raven.contrib.flask import Sentry

from alps.config import read_config
from alps.db import session, setup_session
from alps.forms import login_error_msg, SignInForm
from alps.model import import_all_modules
from alps.user import User


__all__ = 'app', 'initialize_app', 'login_manager'

import_all_modules()

app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()
csrf_protect = CsrfProtect()

setup_session(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf_protect.init_app(app)


def initialize_app(app=None, config_dict=None):
    if app is None:
        raise ValueError('argument app is missing or None')
    if config_dict is None:
        raise ValueError('argument config_dict is missing or None')
    if not isinstance(config_dict, collections.abc.Mapping):
        raise ValueError('argument config_dict is not a dictionary type')
    app.config.update(config_dict)

    sentry = Sentry(dsn=app.config['SENTRY_DSN'])
    sentry.init_app(app)


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/secret')
@login_required
def secret_page():
    return 'Welcome to my secret page. This is for test.'
