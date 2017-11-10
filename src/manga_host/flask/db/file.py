from .common import conn, update_not_null


def create(manga_id, url, location=None, downloaded=False, ignore=False, parsed=False):
    with conn.cursor() as cur:
        try:
            cur.execute(
                'INSERT INTO files (manga_id, url, location, downloaded, ignore, parsed) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (manga_id, url, location, downloaded, ignore, parsed),
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


def update(file_id, manga_id=None, url=None, location=None, downloaded=None, ignore=None, parsed=None):
    return update_not_null(
        table_name='files',
        args={
            'manga_id': manga_id,
            'url': url,
            'location': location,
            'downloaded': downloaded,
            'ignore': ignore,
            'parsed': parsed,
        },
        condition=('file_id', file_id),
    )


def delete(file_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM files WHERE file_id = %s', (file_id,))

    conn.commit()


def index(manga_id):
    with conn.cursor() as cur:
        cur.execute('SELECT file_id, url, location, downloaded, ignore, parsed FROM files WHERE manga_id = %s',
                    (manga_id,))
        return cur.fetchall()
