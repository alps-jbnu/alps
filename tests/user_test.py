from alps.user import User


def test_users_are_created(fx_session, fx_users):
    assert fx_session.query(User).count() == 3
    user = fx_session.query(User).filter_by(nickname='알프스').one()
    assert user == fx_users.user_3


def test_user_password(fx_session, fx_users):
    user = fx_session.query(User).filter_by(nickname='그래').one()
    assert user.check_password('iamayesman')
    assert not user.check_password('idontknowpassword')
