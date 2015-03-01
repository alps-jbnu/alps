from flask import url_for

from alps.forms import (id_len_msg, login_error_msg, id_char_msg,
                        pw_len_msg)


def post_login_form(fx_flask_client, username, password):
        response = fx_flask_client.post(
            url_for('login'),
            data=dict(username=username,
                      password=password),
            follow_redirects=True
        )
        return response


def test_sign_in_form(fx_flask_client, fx_request_context,
                      fx_session, fx_users):
    # 올바른 경우
    response = post_login_form(fx_flask_client, 'yesman', 'iamayesman')
    assert login_error_msg not in response.data.decode(encoding='utf-8')

    # 아이디만 틀린 경우
    response = post_login_form(fx_flask_client, 'noman', 'iamayesman')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')

    # 비밀번호만 틀린 경우
    response = post_login_form(fx_flask_client, 'yesman', 'iamasuperman')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')

    # 아이디에 특수문자를 포함한 경우
    response = post_login_form(fx_flask_client, 'alps!@#$', 'user4password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')

    # 아이디에 공백를 포함한 경우
    response = post_login_form(fx_flask_client, 'alps user', 'user5password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')

    # 아이디가 길이가 알맞지 않은 경우
    response = post_login_form(fx_flask_client, 'alp', 'user6password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')

    # 비밀번호가 길이가 알맞지 않은 경우
    response = post_login_form(fx_flask_client, 'alpsuser', 'user7')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg in response.data.decode(encoding='utf-8')

    # 올바른 경우
    response = post_login_form(fx_flask_client, 'hihi', 'hellohello')
    assert login_error_msg not in response.data.decode(encoding='utf-8')
