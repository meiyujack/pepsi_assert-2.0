from apiflask import APIFlask
from flask import redirect,url_for
from .user import user
from .ledger import ledger

app = APIFlask(__name__, title='固定资产管理系统', version='0.01')

app.secret_key = 'ocefjVp_pL4Iens21FTjsA'
app.env = 'development'

app.register_blueprint(user)
app.register_blueprint(ledger)


@app.get('/')
def index():
    return redirect(url_for('user.login_show'))