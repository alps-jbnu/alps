from flask.ext.wtf import Form
from wtforms import PasswordField, TextField
from wtforms.validators import Regexp, Length

__all__ = 'SignInForm',

no_space_validator = Regexp(
    '^[a-zA-Z0-9_.\\-]*$',
    message="아이디는 영문, 숫자, 일부 특수문자만 가능합니다."
)

id_length_validator = Length(
    min=4,
    max=25,
    message='아이디의 길이는 4자 이상, 25자 이하여야 합니다.'
)

password_length_validator = Length(
    min=4,
    max=50,
    message='비밀번호의 길이는 8자 이상, 50자 이하여야 합니다.'
)


class SignInForm(Form):
    username = TextField('아이디', [no_space_validator, id_length_validator])
    password = PasswordField('패스워드', [password_length_validator])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        if not super().validate():
            return False

        # TODO: Check If username and password is correct!
        return True
