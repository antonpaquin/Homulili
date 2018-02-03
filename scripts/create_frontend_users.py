import sqlite3
import os

import config

if False:
    raise RuntimeError('killswitch -- remove to run, replace when you\'re done')

direction = 'UP'

project_root = os.path.dirname(os.getcwd())
migrations_dir = os.path.join(project_root, 'src/frontend/sqlmigrations/')
database_name = config.user_database

migrations = os.listdir(migrations_dir)
migrations.sort()

if direction == 'DOWN':
    migrations.reverse()

conn = sqlite3.connect(database_name)


def run_migration(f):
    with open(f, 'r') as migration_f:
        query = migration_f.read()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()


for migration in migrations:
    run_migration('{rootpath}/{migration_name}/{direction}.sql'.format(
        rootpath=migrations_dir,
        migration_name=migration,
        direction=('up' if direction == 'UP' else 'down')
    ))
