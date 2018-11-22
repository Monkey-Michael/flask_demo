import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	APP_NAME = os.environ.get('APP_NAME')



class DevelopmentConfig(Config):
	pass

config = {
	"development":DevelopmentConfig
}