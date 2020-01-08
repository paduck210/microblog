import os
basedir = os.path.abspath(os.path.dirname(__file__))


# TODO: * TASK 6: Implement an ORM database access layer so we don’t have SQL in the controller code.
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '111111'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db') # after migration
    SQLALCHEMY_TRACK_MODIFICATIONS = False