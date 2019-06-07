from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session

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