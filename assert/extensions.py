from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    user = User.query.get(int(user_id))
    return users


login_manager.login_view = "user.login_post"
login_manager.login_message_category = "warning"
