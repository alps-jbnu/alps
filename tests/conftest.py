import contextlib
import types

from pytest import fixture, yield_fixture

from alps.app import app
from alps.db import Base, get_engine, get_session
from alps.user import User


def pytest_addoption(parser):
    parser.addoption('--database-url', type='string',
                     help='Database URL for testing')


@contextlib.contextmanager
def _fx_session(engine):
    try:
        metadata = Base.metadata
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)
        session = get_session(engine)
        yield session
        session.rollback()
        metadata.drop_all(bind=engine)
    finally:
        engine.dispose()


@yield_fixture
def fx_session(request):
    database_url = request.config.getoption('--database-url') or \
        'sqlite://'

    with _fx_session(engine=get_engine(database_url=database_url)) as sess:
        yield sess


@fixture
def fx_flask_client(fx_session):
    return app.test_client()


class FixtureModule(types.ModuleType):

    def __add__(self, module):
        clone = type(self)(self.__name__, self.__doc__)
        clone += self
        clone += module
        return clone

    def __iadd__(self, module):
        for name in dir(module):
            if not name.startswith('_'):
                setattr(self, name, getattr(module, name))
        return self


@fixture
def fx_users(fx_session):
    f = FixtureModule('fx_users')

    f.user_1 = User(name='철수')
    f.user_2 = User(name='영희')
    f.user_3 = User(name='알프스')

    with fx_session.begin():
        fx_session.add_all([f.user_1, f.user_2, f.user_3])
    return f
