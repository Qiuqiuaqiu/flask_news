from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from config import configs
import logging


db = SQLAlchemy()

def set_log(config_name):
    logging.basicConfig(level=configs[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

redis_store = None #type:StrictRedis

def create_app(config_name):

    set_log(config_name)

    app = Flask(__name__)
    # 1.设置app的配置
    app.config.from_object(configs[config_name])
    # 2.设置sqlalchemy
    db.init_app(app)
    # 3.集成redis，可以把容易变化的值存入redis
    global redis_store
    redis_store = StrictRedis(host=configs[config_name].REDIS_HOST,port=configs[config_name].REDIS_PORT)
    # 4.CSRFProtect，只起到保护作用！具体往表单和cookie中设置csrf_token还需要我们自己去做
    CSRFProtect(app)
    #5.flask中的session是保存用户数据的容器（上下文），而flask_session中的Session是指定session的保存路径
    Session(app)

    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    return app