import collections.abc
import os
import pathlib

from flask import Flask, render_template
from flask.ext.login import LoginManager

from alps.config import read_config
from alps.db import setup_session


__all__ = 'app', 'initialize_app'

app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()

setup_session(app)
login_manager.init_app(app)


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
