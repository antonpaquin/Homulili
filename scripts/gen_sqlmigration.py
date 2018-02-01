import os
from datetime import datetime

if True:
    raise RuntimeError('killswitch -- remove to run, replace when you\'re done')
    pass

name = 'api tokens'
migration_dir = 'src/manga_host/sqlmigrations/'

# fmt name into a reasonable directory name
name = name.replace(' ', '_')

# Root of the entire project
project_root = os.path.dirname(os.getcwd())

# UTC Timestamp
timestamp = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())

# Name of the migration dir
migration_name = '{timestamp}_{name}'.format(timestamp=timestamp, name=name)

# Full path of the new dir
target_name = os.path.join(project_root, migration_dir, migration_name)
os.mkdir(target_name)

# Make the sql files
with open(os.path.join(target_name, 'up.sql'), 'w'):
    pass

with open(os.path.join(target_name, 'down.sql'), 'w'):
    pass
