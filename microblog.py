import os
from flask_script import Manager # pip install Flask-Script
from flask_migrate import Migrate, MigrateCommand
from myapp import app, db
from myapp.models import User, Post


# TODO Task2. Write a database migration script in `resources/`
MIGRATION_DIR = os.path.join('resources')
migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# set default in flask shell; import db, User, Post
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
