from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

#from auth import WebSecurity

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

#web_secure=WebSecurity()


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    user = User.query.get(int(user_id))
    return user


login_manager.login_view = "user.login"
login_manager.login_message_category = "warning"
