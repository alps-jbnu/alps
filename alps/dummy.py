from alps.db import session
from alps.model import import_all_modules
from alps.user import User


def insert_dummy_data(app):
    import_all_modules()

    user_1 = User(username='yesman', name='장그래', nickname='그래',
                  email='yes@alps.jbnu.ac.kr')
    user_1.set_password('iamayesman')
    user_2 = User(username='hihi', name='안영이', nickname='안녕',
                  email='hi@alps.jbnu.ac.kr')
    user_2.set_password('hellohello')
    user_3 = User(username='alps', name='알프스', nickname='알프스',
                  email='alps@alps.jbnu.ac.kr')
    user_3.set_password('alpspassword')

    with app.app_context():
        with session.begin():
            session.add_all([user_1, user_2, user_3])
