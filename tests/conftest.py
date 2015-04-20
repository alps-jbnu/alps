import contextlib
import types

from pytest import fixture, yield_fixture

from alps.app import app, initialize_app
from alps.db import Base, get_engine, get_session
from alps.post import Board, Post
from alps.user import MemberType, User


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
             USE_SENTRY=False,
             SEND_MAIL=False)
    )
    initialize_app(app)
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
    f.user_1 = User(
        username='yesman',
        nickname='그래',
        email='yes@alps.jbnu.ac.kr',
        name='장그래',
        description='안녕하세요. 장그래입니다.',
        email_validated=True,
        member_type=MemberType.non_member.value,
    )
    f.user_1.set_password('iamayesman')

    f.user_2 = User(
        username='hihi',
        nickname='안녕',
        email='hi@alps.jbnu.ac.kr',
        name='안영이',
        email_validated=True,
        member_type=MemberType.member.value,
    )
    f.user_2.set_password('hellohello')

    f.alps_user = User(
        username='alps',
        nickname='알프스',
        email='alps@alps.jbnu.ac.kr',
        name='알프스',
        description='알프스입니다.',
        is_jbnu_student=True,
        student_number='101512345',
        department='컴퓨터공학부',
        email_validated=True,
        member_type=MemberType.executive.value,
    )
    f.alps_user.set_password('alpspassword')

    with fx_session.begin():
        fx_session.add_all([f.user_1, f.user_2, f.alps_user])
    return f


@fixture
def fx_boards(fx_session):
    f = FixtureModule('fx_boards')

    f.free_board = Board(name='free', text='자유게시판')
    f.member_board = Board(name='member', text='회원게시판',
                           read_permission=MemberType.member.value,
                           write_permission=MemberType.member.value)
    f.executive_board = Board(name='executive', text='임원게시판',
                              read_permission=MemberType.executive.value,
                              write_permission=MemberType.executive.value)

    with fx_session.begin():
        fx_session.add_all([f.free_board, f.member_board, f.executive_board])
    return f


@fixture
def fx_posts(fx_session, fx_boards, fx_users):
    f = FixtureModule('fx_posts')

    f.free_post_1 = Post(
        title='첫 게시글입니다.',
        content='안녕하세요. 테스트를 위한 글입니다.',
        user=fx_users.user_1,
        board=fx_boards.free_board
    )
    f.member_post_1 = Post(
        title='회원 여러분께 드릴 말씀이 있습니다.',
        content='안녕하세요? 같이 열심히 공부해봅시다.',
        user=fx_users.user_2,
        board=fx_boards.member_board
    )
    f.executive_post_1 = Post(
        title='이 곳은 임원게시판입니다.',
        content='임원에게만 공개할 중요한 게시글을 이 곳에 작성하세요.',
        user=fx_users.alps_user,
        board=fx_boards.executive_board
    )
    f.free_post_2 = Post(
        title='2015 알프스 신입회원 모집',
        content='신입회원을 모집합니다.',
        user=fx_users.alps_user,
        board=fx_boards.free_board
    )

    with fx_session.begin():
        fx_session.add_all([f.free_post_1, f.free_post_2,
                            f.member_post_1, f.executive_post_1])
    return f
