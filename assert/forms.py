from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DateField,
    SelectField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    userid = StringField("Userid", validators=[DataRequired(), Length(6, 6)])
    password = PasswordField("Password", validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField("登录")


class SignupForm(LoginForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 20)])
    submit = SubmitField("注册")


class PersonalForm(FlaskForm):
    assert_type = SelectField("assert_type", coerce=int, default=1)
    assert_id = StringField("assert_id", validators=[DataRequired()])
    assert_name = StringField("assert_name", validators=[DataRequired()])
    assert_model = StringField("assert_model", validators=[DataRequired()])
    YoN = BooleanField("YoN", validators=[DataRequired()], default=False)
    bought_date = DateField("bought_date", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (2, "办公家具"),
            (3, "电脑及打印机"),
            (4, "家电"),
            (6, "数码产品"),
            (8, "其他"),
        ]


class PublicForm(PersonalForm):
    def __init__(self, *args, **kwargs):
        super(PublicForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.query.all())]
