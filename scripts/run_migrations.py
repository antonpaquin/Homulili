import os

if False:
    raise RuntimeError('killswitch -- remove to run, replace when you\'re done')
    pass

# TODO implement this with a migrations table that knows the state of all these files
direction = 'UP'

assert direction == 'UP' or direction == 'DOWN'

project_root = os.path.dirname(os.getcwd())
migrations_dir = os.path.join(project_root, 'src/manga_host/sqlmigrations')

migrations = os.listdir(migrations_dir)
migrations.sort()

if direction == 'DOWN':
    migrations.reverse()

def run_migration(f):
    os.system('psql -d manga_project -a -f {file}'.format(file=f))

for migration in migrations:
    run_migration('{rootpath}/{migration_name}/{direction}.sql'.format(
        rootpath=migrations_dir,
        migration_name=migration,
        direction=('up' if direction == 'UP' else 'down')
    ))

