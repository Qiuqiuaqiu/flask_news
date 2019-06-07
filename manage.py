from flask import Flask, session

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand


from info import app,db

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