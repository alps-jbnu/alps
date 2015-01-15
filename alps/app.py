import collections.abc

from flask import Flask, render_template

__all__ = 'app', 'initialize_app'

app = Flask(__name__, template_folder='templates')


def initialize_app(app=None, config_dict=None):
    if app is None:
        raise ValueError('argument app is missing or None')
    if config_dict is None:
        raise ValueError('argument config_dict is missing or None')
    if not isinstance(config_dict, collections.abc.Mapping):
        raise ValueError('argument config_dict is not a dictionary type')
    app.config.update(config_dict)


@app.route('/')
def index():
    return render_template('index.html', msg='Hello, ALPS!')
