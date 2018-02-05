#! /usr/bin/python3

import sqlite3
from datetime import datetime
import os
import sys

import secret
import config

project_root = os.path.dirname(os.getcwd())
migration_db_path = os.path.join(project_root, 'src', 'sqlmigrations.db')


def create_migration_tables():
    conn = sqlite3.connect(migration_db_path)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE migrations ( 
            tstamp INT,
            name TEXT,
            state TEXT,
            project TEXT
        );
    ''')
    cur.close()
    conn.commit()
    conn.close()


def import_migrations():
    if not migration_table_exists():
        create_migration_tables()

    locations = [(os.path.join(project_root, 'src', x, 'sqlmigrations'), x) for x in ['backend', 'frontend', 'cdn']]
    for location, project in locations:
        migrations = os.listdir(location)
        for m_dirname in migrations:
            tstamp = int(m_dirname[:m_dirname.find('_')])
            name = m_dirname[m_dirname.find('_')+1:]
            if migration_exists(project, name, tstamp):
                print('Refusing to import {tstamp}_{name} -- already exists'.format(tstamp=tstamp, name=name))
            else:
                print('Importing {tstamp}_{name}'.format(tstamp=tstamp, name=name))
                add_migration(project, name, tstamp)


def create_migration(project, name):
    name = fmt_name(name)
    timestamp = current_timestamp()

    create_migration_files(project, name, timestamp)
    add_migration(project, name, timestamp)


def add_migration(project, name, timestamp, state='down'):
    assert migration_table_exists(), 'Create the table first'
    assert state in {'up', 'down'}, 'Invalid state -- (up|down)'
    assert project in {'backend', 'frontend', 'cdn'}, 'Invalid project -- (backend|frontend|cdn)'

    conn = sqlite3.connect(migration_db_path)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO migrations (tstamp, name, state, project) VALUES (?, ?, ?, ?)',
        (timestamp, name, state, project),
    )
    cur.close()
    conn.commit()
    conn.close()


def run_migration(m_id, direction='up'):
    assert migration_table_exists(), 'Create the table first'
    assert direction in {'up', 'down'}, 'Invalid direction -- (up|down)'

    conn = sqlite3.connect(migration_db_path)
    cur = conn.cursor()
    cur.execute(
        'SELECT tstamp, name, state, project FROM migrations WHERE rowid = ?',
        (m_id,),
    )
    results = cur.fetchone()
    assert results, 'Invalid migration'

    tstamp, name, state, project = results
    if state == direction:
        print('Bypassing {timestamp}_{name} -- already run'.format(timestamp=tstamp, name=name))
        cur.close()
        conn.close()
        return

    if direction == 'up':
        cur.execute(
            "SELECT 1 FROM migrations WHERE state = 'down' AND tstamp < ?",
            (tstamp,),
        )
    else:
        cur.execute(
            "SELECT 1 FROM migrations WHERE state = 'up' AND tstamp > ?",
            (tstamp,),
        )
    results = cur.fetchone()
    assert not results, 'Refusing to execute out of order'

    full_path = get_migration_path(project, tstamp, name, direction)

    assert os.path.isfile(full_path), 'Migration is not present'

    print('Running migration {timestamp}_{name}'.format(timestamp=tstamp, name=name))

    if project == 'backend':
        os.environ['PGPASSWORD'] = secret.postgres_password
        os.system('psql -X -U homulili -h 127.0.0.1 -f {file} --echo-all homulili'.format(file=full_path))
        os.environ['PGPASSWORD'] = ''
    elif project == 'cdn':
        os.environ['PGPASSWORD'] = secret.postgres_password
        os.system('psql -X -U homulili -h 127.0.0.1 -f {file} --echo-all homulili_cdn'.format(file=full_path))
        os.environ['PGPASSWORD'] = ''
    else:
        os.system('cat {file} | sqlite3 {database}'.format(
            file=full_path,
            database=config.user_database,
        ))

    cur.execute(
        'UPDATE migrations SET state = ? WHERE rowid = ?',
        (direction, m_id),
    )
    cur.close()
    conn.commit()
    conn.close()


def get_migrations(project, ts_min=0, ts_max=2**31, order='asc'):
    assert project in {'backend', 'frontend', 'cdn'}, 'Invalid project -- (backend|frontend|cdn)'
    assert order in {'asc', 'desc'}, 'Invalid order -- (asc|desc)'
    conn = sqlite3.connect(migration_db_path)
    cur = conn.cursor()
    cur.execute(
        'SELECT rowid, tstamp FROM migrations WHERE project = ? AND tstamp BETWEEN ? AND ?',
        (project, ts_min, ts_max),
    )
    results = cur.fetchall()
    cur.close()
    conn.close()

    results = sorted(results, key=lambda r: r[1], reverse=(False if order == 'asc' else True))
    results = [r[0] for r in results]

    return results


def run_migrations(project, direction, ts_min=0, ts_max=2**31):
    if direction == 'up':
        migrations = get_migrations(project, ts_min, ts_max, 'asc')
    else:
        migrations = get_migrations(project, ts_min, ts_max, 'desc')

    for m in migrations:
        run_migration(m, direction)


def describe_migrations(project):
    assert migration_table_exists(), 'Create the table first'
    assert project in {'backend', 'frontend', 'cdn'}, 'Invalid project -- (backend|frontend|cnd)'

    conn = sqlite3.connect(migration_db_path)
    cur = conn.cursor()
    cur.execute(
        'SELECT project, tstamp, name, state FROM migrations WHERE project = ?',
        (project,),
    )
    results = cur.fetchall()
    cur.close()
    conn.close()

    if not results:
        print('Emtpy')
        return

    results = sorted(results, key=lambda x: x[1])
    for row in results:
        print('{tstamp} {name} {pstate}'.format(
            tstamp=rightpad(12, str(row[1])),
            name=rightpad(40, row[2]),
            pstate=rightpad(10, row[3]),
        ))


def create_migration_files(project, name, timestamp):
    up = get_migration_path(project, timestamp, name, 'up')
    down = get_migration_path(project, timestamp, name, 'down')
    mdir = os.path.dirname(up)

    os.mkdir(mdir)
    with open(up, 'w'):
        pass
    with open(down, 'w'):
        pass


def migration_table_exists():
    return os.path.isfile(migration_db_path)


def migration_exists(project, name, tstamp):
    conn = sqlite3.connect(migration_db_path)
    cur = conn.cursor()
    cur.execute(
        'SELECT 1 FROM migrations WHERE project = ? AND tstamp = ? AND name = ?',
        (project, tstamp, name),
    )
    results = cur.fetchone()
    cur.close()
    conn.close()
    return bool(results)


def get_migration_path(project, tstamp, name, direction):
    mdir = os.path.join(project_root, 'src', project, 'sqlmigrations')
    mname = '{tstamp}_{name}'.format(tstamp=tstamp, name=name)
    mfile = '{direction}.sql'.format(direction=direction)
    return os.path.join(mdir, mname, mfile)


def current_timestamp():
    return int((datetime.now() - datetime(1970, 1, 1)).total_seconds())


def fmt_name(name):
    n = name.strip()
    n = n.replace(' ', '_')
    return n


def rightpad(length, key):
    if len(key) > length:
        return key
    return key + (' '*(length-len(key)))


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in {'generate', 'import', 'run', 'show'}:
        print('Usage: migrate.py (generate|import|run|show)')
        exit(1)

    if sys.argv[1] == 'generate':
        if len(sys.argv) != 4 or sys.argv[2] not in {'backend', 'frontend', 'cdn'}:
            print('Usage: migrate.py generate (backend|frontend|cdn) "migration name"')
            exit(1)
        project = sys.argv[2]
        name = sys.argv[3]
        create_migration(project, name)

    elif sys.argv[1] == 'import':
        if len(sys.argv) != 2:
            print('Usage: migrate.py import')
            exit(1)
        import_migrations()

    elif sys.argv[1] == 'run':
        if (
                len(sys.argv) not in {4, 5}
                or sys.argv[2] not in {'backend', 'frontend', 'cdn'}
                or sys.argv[3] not in {'up', 'down'}
        ):
            print('Usage: migrate.py run (backend|frontend|cdn) (up|down) [timestamp]')
            exit(1)
        project = sys.argv[2]
        direction = sys.argv[3]
        ts_max = 2**31
        ts_min = 0
        if len(sys.argv) == 5 and direction == 'up':
            ts_max = sys.argv[4]
        elif len(sys.argv) == 5 and direction == 'down':
            ts_min = sys.argv[4]
        run_migrations(project, direction, ts_min, ts_max)

    elif sys.argv[1] == 'show':
        if len(sys.argv) != 3 or sys.argv[2] not in {'backend', 'frontend', 'cdn'}:
            print('Usage: migrate.py show (backend|frontend|cdn)')
            exit(1)
        project = sys.argv[2]
        describe_migrations(project)

