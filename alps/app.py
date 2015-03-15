import os
import pathlib

from flask import abort, Flask, redirect, render_template, request, url_for
from flask.ext.login import (LoginManager, login_required, login_user,
                             logout_user)
from flask.ext.mail import Mail, Message
from flask_wtf.csrf import CsrfProtect
from raven.contrib.flask import Sentry

from alps import ayah
from alps.config import read_config
from alps.db import session, setup_session
from alps.forms import login_error_msg, SignInForm, SignUpForm
from alps.model import import_all_modules
from alps.post import Board, Post
from alps.user import User


__all__ = 'app', 'initialize_app', 'login_manager', 'MAX_POSTS_PER_PAGE'

import_all_modules()

app = Flask(__name__, template_folder='templates')
setup_session(app)

login_manager = LoginManager()
csrf_protect = CsrfProtect()
mail = Mail()

MAX_POSTS_PER_PAGE = 20


def initialize_app(app=None, config_dict=None):
    if app is None:
        raise ValueError('argument app is missing or None')

    if config_dict:
        app.config.update(config_dict)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    csrf_protect.init_app(app)
    mail.init_app(app)

    # Make Game Style Embedded.
    # Add your Publisher Key and Scoring Key to Config File.
    if app.config['USE_AYAH']:
        ayah.configure(app.config['AYAH_PUBLISHER_KEY'],
                       app.config['AYAH_SCORING_KEY'])

    # Init Sentry.
    if app.config['USE_SENTRY']:
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


@app.route('/board/<board_name>')
def list_board(board_name):
    return list_board_with_page(board_name=board_name, page=1)


@app.route('/board/<board_name>/<int:page>')
def list_board_with_page(board_name, page):
    board = session.query(Board).filter_by(name=board_name).first()
    if not board:
        abort(404)

    post_cnt = board.posts.count()
    max_page = post_cnt // MAX_POSTS_PER_PAGE
    if (max_page == 0) or (post_cnt % MAX_POSTS_PER_PAGE > 0):
        max_page += 1

    if (page < 1) or (page > max_page):
        abort(404)

    posts = board.posts.order_by(Post.created_at) \
                       .limit(MAX_POSTS_PER_PAGE) \
                       .offset(MAX_POSTS_PER_PAGE * (page-1)) \
                       .all()

    return render_template('board.html', title=board.text,
                           writable=False, posts=posts,
                           max_post_cnt=MAX_POSTS_PER_PAGE)


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
            is_jbnu_student = False
            student_number = None
            department = None
            if form.jbnu_student.data:
                is_jbnu_student = True
                if form.student_number.data:
                    student_number = form.student_number.data
                if form.department.data:
                    department = form.department.data

            # Create new user.
            new_user = User(
                username=form.username.data,
                nickname=form.nickname.data,
                email=form.email.data,
                name=form.name.data,
                description=form.description.data,
                is_jbnu_student=is_jbnu_student,
                student_number=student_number,
                department=department,
            )
            new_user.set_password(form.password.data)
            new_user.generate_confirm_token()

            # Insert the new user.
            with session.begin():
                session.add(new_user)

            # Send confirm mail to the user.
            if app.config['SEND_MAIL']:
                msg_body = render_template(
                    'confirm_mail.html',
                    nickname=new_user.nickname,
                    link=url_for('register_confirm',
                                 confirm_token=new_user.confirm_token,
                                 _external=True),
                    confirm_token=new_user.confirm_token
                )
                msg = Message(
                    '알프스 회원가입 확인',
                    html=msg_body,
                    recipients=[new_user.email]
                )
                msg.sender = app.config['DEFAULT_MAIL_SENDER']
                mail.send(msg)
            else:
                # Skip sending confirm mail
                with session.begin():
                    new_user.email_validated = True
                    new_user.confirm_token = None

            return redirect(url_for('register_complete'))
    elif request.method == 'GET':
        if use_ayah:
            return render_template('register.html', form=form,
                                   ayah=ayah.get_publisher_html())
        else:
            return render_template('register.html', form=form)


@app.route('/register/complete')
def register_complete():
    return render_template('register_complete.html')


@app.route('/register/email_confirmed')
def email_confirmed():
    return render_template('email_confirmed.html')


@app.route('/register/confirm/<confirm_token>')
def register_confirm(confirm_token):
    user = session.query(User).filter_by(confirm_token=confirm_token).first()
    if not user:
        abort(404)

    logout_user()
    user.email_validated = True
    with session.begin():
        user.confirm_token = None  # Delete token
    return redirect(url_for('email_confirmed'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
