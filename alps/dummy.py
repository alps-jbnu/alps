import random

from alps.db import session
from alps.fixture import insert_initial_data
from alps.model import import_all_modules
from alps.user import User
from alps.post import Board, Post

__all__ = 'insert_dummy_data',


def insert_dummy_data(app):
    import_all_modules()
    insert_initial_data(app)

    with app.app_context():
        admin_user = session.query(User) \
                            .filter_by(username='admin') \
                            .first()
        alps_user = session.query(User) \
                           .filter_by(username='alps') \
                           .first()
        free_board = session.query(Board).filter_by(name='free').first()
        member_board = session.query(Board).filter_by(name='member').first()
        qna_board = session.query(Board).filter_by(name='qna').first()

        users = (admin_user, alps_user)
        sentences = (
            '안녕하십니까?', '오랜만입니다.', '잘 지내시죠?', '처음 뵙겠습니다.',
            '만나서 기쁩니다.', '만나 뵙게 되어 영광입니다.', '또 봅시다.',
            '좋은 하루 되세요!', '행운을 빕니다.', '고맙습니다.', '실례합니다.',
            '괜찮습니다.', '저 좀 도와주세요.', '행복하세요!', '안녕하세요.',
            '테스트입니다.', '질문이 있습니다.', '여러분께 드릴 말씀이 있습니다.',
            'Hello, World!', 'This is a test.', 'Have a nice day!',
        )
        boards = (free_board, member_board, qna_board)

        for i in range(random.randrange(100, 201)):
            random_post = Post(
                title=random.choice(sentences),
                content=random.choice(sentences),
                user=random.choice(users),
                board=random.choice(boards)
            )
            with session.begin():
                session.add_all([random_post])
