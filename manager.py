import os
import subprocess

from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager,Shell
from redis import Redis
from rq import Connection,Queue,Worker
from app import create_app,db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
