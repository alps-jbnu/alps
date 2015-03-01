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


def test_proper_login(fx_flask_client, fx_request_context,
                      fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'yesman', 'iamayesman')
    assert login_error_msg not in response.data.decode(encoding='utf-8')

    response = post_login_form(fx_flask_client, 'hihi', 'hellohello')
    assert login_error_msg not in response.data.decode(encoding='utf-8')


def test_login_with_only_wrong_id(fx_flask_client, fx_request_context,
                                  fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'noman', 'iamayesman')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')


def test_login_with_only_wrong_pw(fx_flask_client, fx_request_context,
                                  fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'yesman', 'iamasuperman')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')


def test_login_when_id_has_special_char(fx_flask_client, fx_request_context,
                                        fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'alps!@#$', 'user4password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')


def test_login_when_id_has_space(fx_flask_client, fx_request_context,
                                 fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'alps user', 'user5password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')


def test_login_with_improper_len_of_id(fx_flask_client, fx_request_context,
                                       fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'alp', 'user6password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')


def test_login_with_improper_len_of_pw(fx_flask_client, fx_request_context,
                                       fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'alpsuser', 'user7')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg in response.data.decode(encoding='utf-8')
