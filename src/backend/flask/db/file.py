from .common import conn, update_not_null
import logging

logger = logging.getLogger(__name__)


def create(manga_id, url, location=None, state='ready'):
    with conn.cursor() as cur:
        try:
            cur.execute(
                'INSERT INTO files (manga_id, url, location, state) '
                'VALUES (%s, %s, %s, %s)',
                (manga_id, url, location, state),
            )
        except Exception as e:
            conn.rollback()
            raise e

        cur.execute('SELECT currval(\'files_file_id_seq\')')
        new_id = cur.fetchone()

    conn.commit()
    # noinspection PyUnboundLocalVariable
    return new_id


def read(file_id):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM files WHERE file_id = %s', (file_id,))
        return cur.fetchone()


def update(file_id, manga_id=None, url=None, location=None, state=None):
    return update_not_null(
        table_name='files',
        args={
            'manga_id': manga_id,
            'url': url,
            'location': location,
            'state': state,
        },
        condition=('file_id', file_id),
    )


def delete(file_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM files WHERE file_id = %s', (file_id,))

    conn.commit()


def index(manga_id=None, state=None):
    query = 'SELECT file_id, url, location, state FROM files'
    opts = []

    if any([manga_id, state]):
        query = query + ' WHERE'

    if manga_id:
        query = query + ' manga_id = %s'
        opts.append(manga_id)

    if all([manga_id, state]):
        query = query + ' AND'

    if state:
        query = query + ' state = %s'
        opts.append(state)

    logger.debug('INDEX manga_id={id} state={state}'.format(
        id=manga_id,
        state=state,
    ))

    with conn.cursor() as cur:
        cur.execute(query, opts)

        return cur.fetchall()
