from flask import Flask, render_template

__all__ = 'app',

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html', msg='Hello, ALPS!')
