from flask import session
from info.modules.index import index_blu
# import logging
from info import redis_store

@index_blu.route('/')
def index():
    # logging.error('error')
    session["xxxx"] = "hahah"
    redis_store.set("na","xiaohuahh")
    return 'index'