import os
import subprocess

from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager,Shell
from redis import Redis
from rq import Connection,Queue,Worker
from app import create_app,db
from app.models import Role, User
from config import Config

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,)

manager.add_command('db',MigrateCommand)

def setup_general():
    Role.insert_roles()  #建立admin和user角色
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            #添加admin的用户
            user = User(
                first_name='Admin',
                last_name='Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()

@manager.command
def recreate_db():
    #建立新的数据
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    User.generate_fake(count=number_users)

@manager.command
def setup_dev():
    setup_general()

@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()

@manager.command
def run_worker():
    """Initializes rq task queue"""
    listen = ['default']
    conn = Redis(
        host = app.config['RQ_DEFAULT_HOST'],
        port=app.config['RQ_DEFAULT_PORT'],
        db=0,
        password=app.config['RQ_DEFAULT_PASSWORD'])

    with Connection(conn):
        worker = Worker(map(Queue,listen))
        worker.work()


if __name__ == '__main__':
    manager.run()
