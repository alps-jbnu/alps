from alps.db import session
from alps.model import import_all_modules
from alps.user import MemberType, User
from alps.post import Board, Post

__all__ = 'insert_dummy_data',


def insert_dummy_data(app):
    import_all_modules()

    user_1 = User(
        username='yesman',
        nickname='그래',
        email='yes@alps.jbnu.ac.kr',
        name='장그래',
        description='안녕하세요. 장그래입니다.',
        email_validated=True,
        member_type=MemberType.non_member.value,
    )
    user_1.set_password('iamayesman')

    user_2 = User(
        username='hihi',
        nickname='안녕',
        email='hi@alps.jbnu.ac.kr',
        name='안영이',
        email_validated=True,
        member_type=MemberType.member.value,
    )
    user_2.set_password('hellohello')

    user_3 = User(
        username='alps2',
        nickname='알프스2',
        email='alps2@alps.jbnu.ac.kr',
        name='알프스',
        description='알프스입니다.',
        is_jbnu_student=True,
        student_number='101512345',
        department='컴퓨터공학부',
        email_validated=True,
        member_type=MemberType.executive.value,
    )
    user_3.set_password('alpspassword')

    free_board = Board(name='free2', text='자유게시판')
    member_board = Board(name='member2', text='회원게시판',
                         read_permission=MemberType.member.value,
                         write_permission=MemberType.member.value)
    executive_board = Board(name='executive2', text='임원게시판',
                            read_permission=MemberType.executive.value,
                            write_permission=MemberType.executive.value)

    post_1 = Post(
        title='첫 게시글입니다.',
        content='안녕하세요. 테스트를 위한 글입니다.',
        user=user_2,
        board=free_board
    )
    post_2 = Post(
        title='안녕 세상아!',
        content='야호!',
        user=user_1,
        board=member_board
    )
    post_3 = Post(
        title='Hello, ALPS!',
        content='I just wanted to say hello',
        user=user_3,
        board=executive_board
    )

    with app.app_context():
        with session.begin():
            session.add_all([user_1, user_2, user_3])
            session.add_all([free_board, member_board, executive_board])
            session.add_all([post_1, post_2, post_3])
