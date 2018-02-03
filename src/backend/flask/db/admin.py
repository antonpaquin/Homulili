from .common import conn, update_not_null
import secrets


def _gen_key():
    return ''.join([secrets.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ) for _ in range(30)])


def create(create=False, read=False, update=False, delete=False, index=False, command=False, admin=False):
    new_key = _gen_key()
    with conn.cursor() as cur:
        try:
            cur.execute(
                'INSERT INTO api_access (api_key, p_create, p_read, p_update, p_delete, p_index, p_command, p_admin)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (new_key, create, read, update, delete, index, command, admin)
            )
        except Exception as e:
            conn.rollback()
            raise e

    conn.commit()
    return new_key


def read(api_key):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM api_access WHERE api_key = %s', (api_key,))
        return cur.fetchone()


def update(api_key, create=None, read=None, update=None, delete=None, index=None, command=None, admin=None):
    return update_not_null(
        table_name='api_access',
        args={
            'create': create,
            'read': read,
            'update': update,
            'delete': delete,
            'index': index,
            'command': command,
            'admin': admin,
        },
        condition=('api_key', api_key),
    )


def delete(api_key):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM api_access WHERE api_key = %s', (api_key,))

    conn.commit()
