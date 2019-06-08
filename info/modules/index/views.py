from flask import session, render_template, current_app
from info.modules.index import index_blu
# import logging
from info import redis_store

@index_blu.route('/')
def index():
    # logging.error('error')
    # session["xxxx"] = "hahah"
    # redis_store.set("na","xiaohuahh")
    return render_template('news/index.html')

@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')