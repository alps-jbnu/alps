from flask import url_for

from alps.forms import (id_length_msg, login_error_msg, id_char_msg,
                        password_length_msg)


def test_sign_in_form(fx_flask_client, fx_request_context,
                      fx_session, fx_users):

    def post_form(username, password):
        response = fx_flask_client.post(
            url_for('login'),
            data=dict(username=username,
                      password=password),
            follow_redirects=True
        )
        return response

    # 올바른 경우
    response = post_form('yesman', 'iamayesman')
    assert login_error_msg not in response.data.decode(encoding='utf-8')

    # 아이디만 틀린 경우
    response = post_form('noman', 'iamayesman')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_length_msg not in response.data.decode(encoding='utf-8')
    assert password_length_msg not in response.data.decode(encoding='utf-8')

    # 비밀번호만 틀린 경우
    response = post_form('yesman', 'iamasuperman')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_length_msg not in response.data.decode(encoding='utf-8')
    assert password_length_msg not in response.data.decode(encoding='utf-8')

    # 아이디에 특수문자를 포함한 경우
    response = post_form('alps!@#$', 'user4password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg in response.data.decode(encoding='utf-8')
    assert id_length_msg not in response.data.decode(encoding='utf-8')
    assert password_length_msg not in response.data.decode(encoding='utf-8')

    # 아이디에 공백를 포함한 경우
    response = post_form('alps user', 'user5password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg in response.data.decode(encoding='utf-8')
    assert id_length_msg not in response.data.decode(encoding='utf-8')
    assert password_length_msg not in response.data.decode(encoding='utf-8')

    # 아이디가 길이가 알맞지 않은 경우
    response = post_form('alp', 'user6password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_length_msg in response.data.decode(encoding='utf-8')
    assert password_length_msg not in response.data.decode(encoding='utf-8')

    # 비밀번호가 길이가 알맞지 않은 경우
    response = post_form('alpsuser', 'user7')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_length_msg not in response.data.decode(encoding='utf-8')
    assert password_length_msg in response.data.decode(encoding='utf-8')

    # 올바른 경우
    response = post_form('hihi', 'hellohello')
    assert login_error_msg not in response.data.decode(encoding='utf-8')
