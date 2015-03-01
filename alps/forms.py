import re

from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, TextField
from wtforms.validators import (Email, EqualTo, InputRequired, Length, Regexp,
                                ValidationError)

from alps.db import session
from alps.user import User

__all__ = (
    'email_msg',
    'id_char_msg',
    'id_len_msg',
    'id_required_msg',
    'login_error_msg',
    'name_char_msg',
    'name_len_msg',
    'nickname_char_msg',
    'nickname_len_msg',
    'pw_confirm_msg',
    'pw_len_msg',
    'pw_required_msg',
    'required_field_msg',
    'SignInForm',
    'SignUpForm',
    'student_number_char_msg',
    'student_number_len_msg',
)


class UnicodeLength(object):
    def __init__(self, min, max, message=None):
        self.min = min
        self.max = max
        if not message:
            message = \
                'Field must be between {} and {} characters long.' \
                .format(min, max)
        self.message = message

    def __call__(self, form, field):
        len = 0
        for char in field.data:
            if re.match('[a-zA-Z0-9 ]', char):  # is alphanumeric?
                len += 1
            else:  # assume other characters are unicode.
                len += 2
        if not (self.min <= len and len <= self.max):
            raise ValidationError(self.message)


class OptionalLength(object):
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = \
                'Field must be between {} and {} characters long.' \
                .format(min, max)
        self.message = message

    def __call__(self, form, field):
        if field.data:
            l = len(field.data)
            if l < self.min or self.max != -1 and l > self.max:
                raise ValidationError(self.message)


login_error_msg = (
    '등록되지 않은 아이디이거나, '
    '아이디 또는 비밀번호를 잘못 입력하셨습니다.'
)

required_field_msg = '필수 입력 항목입니다.'
required_validator = InputRequired(message=required_field_msg)

id_required_msg = '아이디를 입력해주세요.'
id_required_validator = InputRequired(message=id_required_msg)

pw_required_msg = '비밀번호를 입력해주세요.'
pw_required_validator = InputRequired(message=pw_required_msg)

id_char_msg = '아이디는 영문, 숫자, 일부 특수문자만 가능합니다.'

# The validator only allows English, Hangul, and numeric characters
# and some special characters: '_', '.' and '-'.
id_char_validator = Regexp('^[a-zA-Z0-9_.\\-]*$',
                           message=id_char_msg)

id_len_msg = '아이디의 길이는 4자 이상, 25자 이하여야 합니다.'
id_len_validator = Length(min=4, max=25,
                          message=id_len_msg)

pw_len_msg = '비밀번호의 길이는 8자 이상, 50자 이하여야 합니다.'
pw_len_validator = Length(min=8, max=50,
                          message=pw_len_msg)

pw_confirm_msg = '비밀번호를 다시 확인해주세요.'
pw_confirm_validator = EqualTo('password', message=pw_confirm_msg)

nickname_char_msg = '닉네임은 영문, 한글, 숫자, 사이 공백만 가능합니다.'

# The validator only allows English, Hangul, digit and whitespace characters.
# But, it doesn't allow leading or trailing whitespace
# and two or more continuous whitespaces.
nickname_char_validator = Regexp(
    '(?!^[ ].*$)(?!^.*[ ]$)(?!^.*[ ]{2,}.*$)^[a-zA-Z0-9ㄱ-ㅣ가-힣 ]*$',
    message=nickname_char_msg
)

nickname_len_msg = '닉네임은 한글 1~10자, 영문 대소문자 2~20자, 숫자를 사용할 수 있습니다. (혼용가능)'
nickname_len_validator = UnicodeLength(min=2,
                                       max=20,
                                       message=nickname_len_msg)

email_msg = '올바른 이메일을 입력해주세요.'
email_validator = Email(message=email_msg)

name_char_msg = '이름에는 한글만 포함할 수 있습니다.'
name_char_validator = Regexp('^[ㄱ-ㅣ가-힣]*$',
                             message=name_char_msg)

name_len_msg = '이름은 2자 이상, 10자 이하여야 합니다.'
name_len_validator = OptionalLength(min=2, max=10,
                                    message=name_len_msg)

student_number_char_msg = '학번은 숫자로만 구성됩니다.'
student_number_char_validator = Regexp('^[0-9]*$',
                                       message=student_number_char_msg)

student_number_len_msg = '학번은 9글자여야 합니다.'
student_number_len_validator = OptionalLength(min=9, max=9,
                                              message=student_number_len_msg)


class SignInForm(Form):
    username = TextField(label='아이디',
                         validators=[id_required_validator,
                                     id_char_validator,
                                     id_len_validator])
    password = PasswordField(label='패스워드',
                             validators=[pw_required_validator,
                                         pw_len_validator])

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
    username = TextField(label='아이디',
                         validators=[required_validator,
                                     id_char_validator,
                                     id_len_validator])
    nickname = TextField(label='닉네임',
                         validators=[required_validator,
                                     nickname_char_validator,
                                     nickname_len_validator])
    email = TextField(label='이메일',
                      validators=[required_validator,
                                  email_validator])
    password = PasswordField(label='패스워드',
                             validators=[required_validator,
                                         pw_len_validator])
    confirm_password = PasswordField(label='패스워드 재확인',
                                     validators=[required_validator,
                                                 pw_confirm_validator])
    name = TextField(label='이름',
                     validators=[name_char_validator,
                                 name_len_validator])
    jbnu_student = BooleanField(label='전북대학교 학생입니까?')
    student_number = TextField(label='학번',
                               validators=[student_number_char_validator,
                                           student_number_len_validator])
    department = TextField(label='학부(과)')
