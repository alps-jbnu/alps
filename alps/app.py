import os
import pathlib

from bleach import clean
from flask import abort, Flask, redirect, render_template, request, url_for
from flask.ext.login import (current_user, LoginManager, login_required,
                             login_user, logout_user)
from flask.ext.mail import Mail, Message
from flask_wtf.csrf import CsrfProtect
from markdown import markdown
from raven.contrib.flask import Sentry

from alps import ayah
from alps.config import read_config
from alps.db import session, setup_session
from alps.forms import (login_error_msg, SignInForm, SignUpForm,
                        WritingPostForm)
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
PAGE_RANGE_LEN = 10

ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                'li', 'ol', 'strong', 'ul', 'img', 'p', 'h1', 'h2', 'h3',
                'h4', 'h5', 'h6', 'br', 'pre', 'table', 'thead', 'tbody',
                'tr', 'th', 'td']
ALLOWED_ATTRIBUTES = {'abbr': ['title'], 'a': ['href', 'title'],
                      'acronym': ['title'], 'img': ['alt', 'src']}


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

    posts = board.posts.order_by(Post.created_at.desc()) \
                       .limit(MAX_POSTS_PER_PAGE) \
                       .offset(MAX_POSTS_PER_PAGE * (page-1)) \
                       .all()

    current_page = page
    start_page = page - ((page-1) % PAGE_RANGE_LEN)
    last_page = min(start_page + PAGE_RANGE_LEN - 1, max_page)
    has_left = True if start_page > 1 else False
    has_right = True if last_page < max_page else False

    writable = False
    if current_user.is_authenticated() and current_user.is_active():
        if current_user.member_type >= board.write_permission:
            writable = True

    readable = False
    if current_user.is_authenticated() and current_user.is_active():
        if current_user.member_type >= board.read_permission:
            readable = True

    return render_template('board.html', title=board.text,
                           writable=writable, readable=readable, posts=posts,
                           max_post_cnt=MAX_POSTS_PER_PAGE,
                           current_page=current_page,
                           start_page=start_page, end_page=last_page+1,
                           has_left=has_left, has_right=has_right,
                           name=board_name)


@app.route('/board/<board_name>/write', methods=['GET', 'POST'])
def write_post(board_name):
    board = session.query(Board).filter_by(name=board_name).first()
    if not board:
        abort(404)

    writable = False
    if current_user.is_authenticated() and current_user.is_active():
        if current_user.member_type >= board.write_permission:
            writable = True
    if not writable:
        abort(404)

    form = WritingPostForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('write_post.html', name=board_name,
                                   text=board.text, form=form)
        else:
            post = Post(board=board, user=current_user,
                        title=form.title.data, content=form.content.data)
            with session.begin():
                session.add(post)
            return redirect(url_for('list_board', board_name=board_name))
    elif request.method == 'GET':
        return render_template('write_post.html', name=board_name,
                               text=board.text, form=form)


@app.route('/board/<board_name>/post/<int:post_id>')
def view_post(board_name, post_id):
    board = session.query(Board).filter_by(name=board_name).first()
    if not board:
        abort(404)

    readable = False
    if current_user.is_authenticated() and current_user.is_active():
        if current_user.member_type >= board.read_permission:
            readable = True
    if not readable:
        abort(404)

    post = session.query(Post).filter_by(id=post_id, board=board).first()
    if not post:
        abort(404)

    next_post = session.query(Post) \
                       .filter(Post.id > post_id, Post.board_id == board.id) \
                       .order_by(Post.id.asc()) \
                       .first()
    prev_post = session.query(Post) \
                       .filter(Post.id < post_id, Post.board_id == board.id) \
                       .order_by(Post.id.desc()) \
                       .first()

    html = markdown(post.content,
                    extensions=['markdown.extensions.nl2br',
                                'markdown.extensions.fenced_code',
                                'markdown.extensions.tables'])
    html = clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

    post_cnt = session.query(Post) \
                      .filter(Post.id > post_id, Post.board_id == board.id) \
                      .count()
    page = post_cnt // MAX_POSTS_PER_PAGE + 1

    return render_template('view_post.html', board=board, post=post,
                           content=html, next_post=next_post,
                           prev_post=prev_post, post_page=page)


@app.route('/board/<board_name>/post/edit/<int:post_id>',
           methods=['GET', 'POST'])
def edit_post(board_name, post_id):
    board = session.query(Board).filter_by(name=board_name).first()
    if not board:
        abort(404)

    writeable = False
    if current_user.is_authenticated() and current_user.is_active():
        if current_user.member_type >= board.write_permission:
            writeable = True
    if not writeable:
        abort(404)

    post = session.query(Post).filter_by(id=post_id, board=board).first()
    if not post:
        abort(404)

    form = WritingPostForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('edit_post.html', name=board_name,
                                   text=board.text, form=form, post=post)
        else:
            with session.begin():
                post.title = form.title.data
                post.content = form.content.data
            return redirect(url_for('view_post', board_name=board_name,
                                    post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('edit_post.html', name=board_name,
                               text=board.text, form=form, post=post)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form,
                                   err_msg=login_error_msg)
        else:
            login_user(load_user(form.username.data), force=True)
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
