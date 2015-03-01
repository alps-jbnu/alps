import re

from flask import url_for

from alps.forms import (
    email_msg,
    id_char_msg,
    id_len_msg,
    id_required_msg,
    login_error_msg,
    name_char_msg,
    name_len_msg,
    nickname_char_msg,
    nickname_len_msg,
    pw_confirm_msg,
    pw_len_msg,
    pw_required_msg,
    required_field_msg,
    student_number_char_msg,
    student_number_len_msg,
)


def post_login_form(fx_flask_client, username, password):
    response = fx_flask_client.post(
        url_for('login'),
        data=dict(username=username,
                  password=password),
        follow_redirects=True
    )
    return response


def post_register_form(fx_flask_client, **kwargs):
    response = fx_flask_client.post(
        url_for('register'),
        data=dict(**kwargs),
        follow_redirects=True
    )
    return response


proper_register_data = dict(
    username='gil-dong',
    nickname='15학번 홍길동b',
    email='jbnu-alps-gildong@gmail.com',
    password='my-new-secret-password',
    confirm_password='my-new-secret-password',
    name='홍길동',
    jbnu_student='y',
    student_number='101599999',
    department='컴퓨터공학부',
)

err_cls_re = re.compile(
    '<[a-z]* .*class=[\'\"][^\'\"]*error[^\'\"]*[\'\"].*>'
)


def test_regex_to_find_error_in_class():
    assert not err_cls_re.search('''
        <div name='abc error' class='erro err e' id='1 error'>error</div>
        ''')
    assert err_cls_re.search('''
        <div name='abc' class='hidden error container' id='1'>abc</div>
        ''')


def test_proper_login(fx_flask_client, fx_request_context,
                      fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'yesman', 'iamayesman')
    assert login_error_msg not in response.data.decode(encoding='utf-8')

    response = post_login_form(fx_flask_client, 'hihi', 'hellohello')
    assert login_error_msg not in response.data.decode(encoding='utf-8')


def test_login_with_wrong_id(fx_flask_client, fx_request_context,
                             fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'noman', 'iamayesman')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_char_msg not in response.data.decode(encoding='utf-8')
    assert id_len_msg not in response.data.decode(encoding='utf-8')
    assert pw_len_msg not in response.data.decode(encoding='utf-8')


def test_login_with_wrong_pw(fx_flask_client, fx_request_context,
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


def test_login_without_id(fx_flask_client, fx_request_context,
                          fx_session, fx_users):
    response = post_login_form(fx_flask_client, '', 'some-password')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert id_required_msg in response.data.decode(encoding='utf-8')


def test_login_without_pw(fx_flask_client, fx_request_context,
                          fx_session, fx_users):
    response = post_login_form(fx_flask_client, 'some-id', '')
    assert login_error_msg in response.data.decode(encoding='utf-8')
    assert pw_required_msg in response.data.decode(encoding='utf-8')


def test_proper_register(fx_flask_client, fx_request_context,
                         fx_session, fx_users):
    data = proper_register_data.copy()
    response = post_register_form(fx_flask_client, **data)
    assert not err_cls_re.search(response.data.decode(encoding='utf-8'))


def test_register_without_id(fx_flask_client, fx_request_context,
                             fx_session, fx_users):
    data = proper_register_data.copy()
    data['username'] = ''
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert required_field_msg in response.data.decode(encoding='utf-8')


def test_register_when_id_has_improper_char(fx_flask_client,
                                            fx_request_context,
                                            fx_session,
                                            fx_users):
    data = proper_register_data.copy()
    data['username'] = 'gil^dong#'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert id_char_msg in response.data.decode(encoding='utf-8')


def test_register_with_improper_len_of_id(fx_flask_client,
                                          fx_request_context,
                                          fx_session,
                                          fx_users):
    data = proper_register_data.copy()
    data['username'] = 'gil'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert id_len_msg in response.data.decode(encoding='utf-8')

    data = proper_register_data.copy()
    data['username'] = '_long_id_len_more_than_25_'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert id_len_msg in response.data.decode(encoding='utf-8')


def test_register_when_nick_has_improper_char(fx_flask_client,
                                              fx_request_context,
                                              fx_session,
                                              fx_users):
    # leading whitespace
    data = proper_register_data.copy()
    data['nickname'] = ' gil'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_char_msg in response.data.decode(encoding='utf-8')

    # trailing whitespace
    data = proper_register_data.copy()
    data['nickname'] = 'gil '
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_char_msg in response.data.decode(encoding='utf-8')

    # special character
    data = proper_register_data.copy()
    data['nickname'] = 'gil!'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_char_msg in response.data.decode(encoding='utf-8')

    # two or more continuous whitespace
    data = proper_register_data.copy()
    data['nickname'] = 'gil  dong'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_char_msg in response.data.decode(encoding='utf-8')


def test_register_with_improper_len_of_nick(fx_flask_client,
                                            fx_request_context,
                                            fx_session,
                                            fx_users):
    data = proper_register_data.copy()
    data['nickname'] = 'g'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_len_msg in response.data.decode(encoding='utf-8')

    data = proper_register_data.copy()
    data['nickname'] = '가나다라마바사아자차a'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_len_msg in response.data.decode(encoding='utf-8')

    data = proper_register_data.copy()
    data['nickname'] = 'abcdevwxyz ABCDEFGHIJ'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_len_msg in response.data.decode(encoding='utf-8')

    data = proper_register_data.copy()
    data['nickname'] = '21 bytes 문자입니다ㅋ'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert nickname_len_msg in response.data.decode(encoding='utf-8')


def test_register_without_nickname(fx_flask_client,
                                   fx_request_context,
                                   fx_session,
                                   fx_users):
    data = proper_register_data.copy()
    data['nickname'] = ''
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert required_field_msg in response.data.decode(encoding='utf-8')


def test_register_with_improper_len_of_pw(fx_flask_client,
                                          fx_request_context,
                                          fx_session,
                                          fx_users):
    data = proper_register_data.copy()
    data['password'] = 'shrt'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert pw_len_msg in response.data.decode(encoding='utf-8')


def test_register_when_confirm_pw_is_not_equal_to_pw(fx_flask_client,
                                                     fx_request_context,
                                                     fx_session,
                                                     fx_users):
    data = proper_register_data.copy()
    data['confirm_password'] = 'different_pw'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert pw_confirm_msg in response.data.decode(encoding='utf-8')


def test_register_with_improper_email(fx_flask_client,
                                      fx_request_context,
                                      fx_session,
                                      fx_users):
    data = proper_register_data.copy()
    data['email'] = 'gildong.gmail.com'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert email_msg in response.data.decode(encoding='utf-8')

    data = proper_register_data.copy()
    data['email'] = 'gildong@gmailcom'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert email_msg in response.data.decode(encoding='utf-8')

    data = proper_register_data.copy()
    data['email'] = '@gmail.com'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert email_msg in response.data.decode(encoding='utf-8')


def test_register_when_name_has_improper_char(fx_flask_client,
                                              fx_request_context,
                                              fx_session,
                                              fx_users):
    data = proper_register_data.copy()
    data['name'] = 'John'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert name_char_msg in response.data.decode(encoding='utf-8')


def test_register_with_improper_len_of_name(fx_flask_client,
                                            fx_request_context,
                                            fx_session,
                                            fx_users):
    data = proper_register_data.copy()
    data['name'] = '홍'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert name_len_msg in response.data.decode(encoding='utf-8')

    data = proper_register_data.copy()
    data['name'] = '가나다라마바사아자차카타파하'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert name_len_msg in response.data.decode(encoding='utf-8')


def test_register_when_student_num_has_not_numerical_char(fx_flask_client,
                                                          fx_request_context,
                                                          fx_session,
                                                          fx_users):
    data = proper_register_data.copy()
    data['student_number'] = '2015a9999'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert student_number_char_msg in response.data.decode(encoding='utf-8')


def test_register_with_improper_len_of_student_num(fx_flask_client,
                                                   fx_request_context,
                                                   fx_session,
                                                   fx_users):
    data = proper_register_data.copy()
    data['student_number'] = '2015123456'
    response = post_register_form(fx_flask_client, **data)
    assert err_cls_re.search(response.data.decode(encoding='utf-8'))
    assert student_number_len_msg in response.data.decode(encoding='utf-8')
