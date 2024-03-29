from redis import StrictRedis
import logging

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

class DevelopConfig(Config):
    LOG_LEVEL = logging.DEBUG

class ProductConfig(Config):
    LOG_LEVEL = logging.ERROR

class TestingConfig(Config):
    pass

configs = {
    "develop" : DevelopConfig,
    "product" : ProductConfig,
    "testing" : TestingConfig

}