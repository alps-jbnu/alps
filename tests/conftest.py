import contextlib
import types

from pytest import fixture, yield_fixture

from alps.app import app
from alps.db import Base, get_engine, get_session
from alps.post import Post
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
        session = get_session(engine=engine)
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
    app.config.update(
        dict(SECRET_KEY='pytest',
             TESTING=True,
             WTF_CSRF_ENABLED=False,
             TEST_SESSION=fx_session,
             USE_AYAH=False,
             USE_SENTRY=False)
    )
    return app.test_client()


@yield_fixture
def fx_request_context(fx_flask_client):
    ctx = app.test_request_context()
    ctx.push()
    yield ctx
    ctx.pop()


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

    # 사용자를 추가합니다.
    f.user_1 = User(username='yesman', name='장그래', nickname='그래',
                    email='yes@alps.jbnu.ac.kr')
    f.user_1.set_password('iamayesman')
    f.user_2 = User(username='hihi', name='안영이', nickname='안녕',
                    email='hi@alps.jbnu.ac.kr')
    f.user_2.set_password('hellohello')
    f.user_3 = User(username='alps', name='알프스', nickname='알프스',
                    email='alps@alps.jbnu.ac.kr')
    f.user_3.set_password('alpspassword')

    # 아래는 폼 테스트를 위한 잘못된 사용자입니다. (로그인조차 불가능)
    f.user_4 = User(username='alps!@#$', name='익명',
                    nickname='특수문자ID유저',
                    email='user4@alps.jbnu.ac.kr')
    f.user_4.set_password('user4password')
    f.user_5 = User(username='alps user', name='익명',
                    nickname='공백ID유저',
                    email='user5@alps.jbnu.ac.kr')
    f.user_5.set_password('user5password')
    f.user_6 = User(username='alp', name='익명',
                    nickname='짧은ID유저',
                    email='user6@alps.jbnu.ac.kr')
    f.user_6.set_password('user6password')
    f.user_7 = User(username='alpsuser', name='익명',
                    nickname='짧은패스워드유저',
                    email='user7@alps.jbnu.ac.kr')
    f.user_7.set_password('user7')

    with fx_session.begin():
        fx_session.add_all([f.user_1, f.user_2, f.user_3])
    return f


@fixture
def fx_posts(fx_session, fx_users):
    f = FixtureModule('fx_posts')

    f.post_1 = Post(
        title='첫 게시글입니다.',
        content='안녕하세요. 테스트를 위한 글입니다.',
        user=fx_users.user_1
    )
    f.post_2 = Post(
        title='안녕 세상아!',
        content='야호!',
        user=fx_users.user_1
    )
    f.post_3 = Post(
        title='Hello, ALPS!',
        content='I just wanted to say hello',
        user=fx_users.user_3
    )

    with fx_session.begin():
        fx_session.add_all([f.post_1, f.post_2, f.post_3])
    return f
