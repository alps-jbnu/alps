from alps.db import session
from alps.model import import_all_modules
from alps.user import User


def insert_dummy_data(app):
    import_all_modules()

    user_1 = User(
        username='yesman',
        nickname='그래',
        email='yes@alps.jbnu.ac.kr',
        name='장그래',
        description='안녕하세요. 장그래입니다.'
    )
    user_1.set_password('iamayesman')

    user_2 = User(
        username='hihi',
        nickname='안녕',
        email='hi@alps.jbnu.ac.kr',
        name='안영이',
    )
    user_2.set_password('hellohello')

    user_3 = User(
        username='alps',
        nickname='알프스',
        email='alps@alps.jbnu.ac.kr',
        name='알프스',
        description='알프스입니다.',
        is_jbnu_student=True,
        student_number='101512345',
        department='컴퓨터공학부',
    )
    user_3.set_password('alpspassword')

    with app.app_context():
        with session.begin():
            session.add_all([user_1, user_2, user_3])
