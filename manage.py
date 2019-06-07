from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand


app = Flask(__name__)

class Config(object):
    SECRET_KEY = "123456"

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/flask_news"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 指定session的存储方式
    SESSION_TYPE = "redis"
    # 指定储存session的储存对象
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 设置session签名 加密
    SESSION_USE_SIGNER = True
    # 设置session永久保存
    SESSION_PERMANENT = False
    # 设置session存储时间
    PERMANENT_SESSION_LIFETIME = 86400*2

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