import collections.abc
import os
import pathlib

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect

from alps.config import read_config
from alps.db import setup_session
from alps.forms import SignInForm


__all__ = 'app', 'initialize_app'

app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()
csrf_protect = CsrfProtect()

setup_session(app)
login_manager.init_app(app)
csrf_protect.init_app(app)

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


try:
    env_config = os.environ['ALPS_CONFIG']
    config_dict = read_config(pathlib.Path(os.environ['ALPS_CONFIG']))
    initialize_app(app, config_dict)
except KeyError:
    pass


@app.route('/')
def index():
    return render_template('index.html', msg='Hello, ALPS!')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)
