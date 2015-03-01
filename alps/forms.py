from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, TextField
from wtforms.validators import Regexp, Length

from alps.db import session
from alps.user import User

__all__ = ('id_length_msg', 'login_error_msg', 'id_char_msg',
           'password_length_msg', 'SignInForm', 'SignUpForm')

login_error_msg = (
    '등록되지 않은 아이디이거나, '
    '아이디 또는 비밀번호를 잘못 입력하셨습니다.'
)

id_char_msg = '아이디는 영문, 숫자, 일부 특수문자만 가능합니다.'
id_char_validator = Regexp('^[a-zA-Z0-9_.\\-]*$',
                           message=id_char_msg)

id_length_msg = '아이디의 길이는 4자 이상, 25자 이하여야 합니다.'
id_length_validator = Length(min=4, max=25,
                             message=id_length_msg)

password_length_msg = '비밀번호의 길이는 8자 이상, 50자 이하여야 합니다.'
password_length_validator = Length(min=8, max=50,
                                   message=password_length_msg)


class SignInForm(Form):
    username = TextField(label='아이디',
                         validator=[id_char_validator, id_length_validator])
    password = PasswordField(label='패스워드',
                             validator=[password_length_validator])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        if not super().validate():
            return False

        # Get user
        user = session.query(User) \
                      .filter_by(username=self.username.data) \
                      .first()
        if not user:
            self.errors.update(
                {'no_field': ['Incorrect username or password']}
            )
            return False

        # Check password
        if not user.check_password(self.password.data):
            self.errors.update(
                {'no_field': ['Incorrect username or password']}
            )
            return False

        return True


class SignUpForm(Form):
    # TODO: more arguments required in the below fields!

    username = TextField(label='아이디', )
    nickname = TextField(label='닉네임')
    email = TextField(label='이메일')
    password = PasswordField(label='패스워드')
    confirm_password = PasswordField(label='패스워드 재확인')
    name = TextField(label='이름')
    jbnu_student = BooleanField(label='전북대학교 학생입니까?')
    student_number = TextField(label='학번')
    department = TextField(label='학부(과)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        if not super().validate():
            return False

        # TODO: validate me!

        return True
