from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand


app = Flask(__name__)

from config import Config

# 1.设置app的配置
app.config.from_object(Config)
# 2.设置sqlalchemy
db = SQLAlchemy(app)
# 3.集成redis，可以把容易变化的值存入redis
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 4.CSRFProtect，只起到保护作用！具体往表单和cookie中设置csrf_token还需要我们自己去做
CSRFProtect(app)
#5.flask中的session是保存用户数据的容器（上下文），而flask_session中的Session是指定session的保存路径
Session(app)
#6.设置Manage
manage = Manager(app)
# 设置migrate
Migrate(app,db)
manage.add_command("db",MigrateCommand)

@app.route('/')
def index():
    session["xxxx"] = "hahah"
    return 'index'

if __name__ == '__main__':
    manage.run()