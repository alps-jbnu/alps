

def test_users_are_created(fx_session, fx_users):
    assert fx_users.user_1.name == '철수'
    assert fx_users.user_2.name == '영희'
    assert fx_users.user_3.name == '알프스'
