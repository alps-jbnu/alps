from alps.db import session
from alps.model import import_all_modules
from alps.user import MemberType, User
from alps.post import Board

__all__ = 'insert_initial_data',


def insert_initial_data(app):
    import_all_modules()

    with app.app_context():
        # 어드민 계정
        admin_user = session.query(User) \
                            .filter_by(username='admin') \
                            .first()
        if not admin_user:
            admin_user = User(
                username='admin',
                nickname='관리자',
                email='admin@alps.jbnu.ac.kr',
                name='관리자',
                email_validated=True,
                member_type=MemberType.admin.value,
            )
            admin_user.set_password('12345678')
            with session.begin():
                session.add(admin_user)
            print('admin 계정이 생성되었습니다. 비밀번호를 변경해주세요! (초기 비밀번호: 12345678)')

        # 알프스 계정
        alps_user = session.query(User) \
                           .filter_by(username='alps') \
                           .first()
        if not alps_user:
            alps_user = User(
                username='alps',
                nickname='알프스',
                email='alps.jbnu@gmail.com',
                name='알프스',
                email_validated=True,
                member_type=MemberType.admin.value,
            )
            alps_user.set_password('12345678')
            with session.begin():
                session.add(alps_user)
            print('alps 계정이 생성되었습니다. 비밀번호를 변경해주세요! (초기 비밀번호: 12345678)')

        # 공지사항
        notice_board = session.query(Board) \
                              .filter_by(name='notice') \
                              .first()
        if not notice_board:
            notice_board = Board(name='notice', text='공지사항',
                                 write_permission=MemberType.executive.value)
            with session.begin():
                session.add(notice_board)
            print('공지사항 게시판이 생성되었습니다.')

        # 자유게시판
        free_board = session.query(Board) \
                            .filter_by(name='free') \
                            .first()
        if not free_board:
            free_board = Board(name='free', text='자유게시판')
            with session.begin():
                session.add(free_board)
            print('자유게시판이 생성되었습니다.')

        # 회원게시판
        member_board = session.query(Board) \
                              .filter_by(name='member') \
                              .first()
        if not member_board:
            member_board = Board(name='member', text='회원게시판',
                                 read_permission=MemberType.member.value,
                                 write_permission=MemberType.member.value)
            with session.begin():
                session.add(member_board)
            print('회원게시판이 생성되었습니다.')

        # 질문과 답변
        qna_board = session.query(Board) \
                           .filter_by(name='qna') \
                           .first()
        if not qna_board:
            qna_board = Board(name='qna', text='질문과 답변')
            with session.begin():
                session.add(qna_board)
            print('질문과 답변 게시판이 생성되었습니다.')
