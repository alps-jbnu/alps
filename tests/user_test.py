from alps.user import User


def test_users_are_created(fx_session, fx_users):
    assert fx_session.query(User).count() == 3
    assert fx_session.query(User).filter_by(nickname='알프스').one() == \
        fx_users.user_3
