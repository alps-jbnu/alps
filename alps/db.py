from flask import current_app, g
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.local import LocalProxy


__all__ = 'Base', 'get_engine', 'get_session', 'Session'

Base = declarative_base()
Session = sessionmaker(autocommit=True)


def get_engine(database_url):
    if database_url:
        return create_engine(database_url)

    config = current_app.config
    try:
        return config['DATABASE_ENGINE']
    except KeyError:
        db_url = config['DATABASE_URL']
        engine = create_engine(db_url)
        config['DATABASE_ENGINE'] = engine
        return engine


def get_session(engine):
    if engine:
        return Session(bind=engine)

    if hasattr(g, 'session'):
        return g.session
    session = Session(bind=get_engine())
    g.session = session


def close_session(exception=None):
    if hasattr(g, 'session'):
        g.session.close()


def setup_session(app):
    app.teardown_appcontext(close_session)


#: (:class:`~werkzeug.local.LocalProxy`)
#: The session will be created on a per-request. Use this.
#: See <http://flask.pocoo.org/docs/0.10/appcontext/> if you wonder.
session = LocalProxy(get_session)
