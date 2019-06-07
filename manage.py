
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from info import create_app,db

app = create_app("develop")

#6.设置Manage
manage = Manager(app)
# 设置migrate
Migrate(app,db)
manage.add_command("db",MigrateCommand)


if __name__ == '__main__':
    manage.run()