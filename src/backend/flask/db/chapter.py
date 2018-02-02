from .common import conn, update_not_null


def create(chapter_name, manga_id, sort_key=0):
    with conn.cursor() as cur:
        try:
            cur.execute(
                'INSERT INTO chapters (chapter_name, manga_id, sort_key) VALUES (%s, %s, %s)',
                (chapter_name, manga_id, sort_key),
            )
        except Exception as e:
            conn.rollback()
            raise e

        cur.execute('SELECT currval(\'chapters_chapter_id_seq\')')
        new_id = cur.fetchone()

    conn.commit()
    # noinspection PyUnboundLocalVariable
    return new_id


def read(chapter_id):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM chapters WHERE chapter_id = %s', (chapter_id,))
        return cur.fetchone()


def update(chapter_id, manga_id=None, chapter_name=None, sort_key=None):
    return update_not_null(
        table_name='chapters',
        args={
            'manga_id': manga_id,
            'chapter_name': chapter_name,
            'sort_key': sort_key,
        },
        condition=('chapter_id', chapter_id),
    )


def delete(chapter_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM chapters WHERE chapter_id = %s', (chapter_id,))

    conn.commit()


def index(manga_id):
    with conn.cursor() as cur:
        cur.execute('SELECT chapter_id, chapter_name, sort_key FROM chapters WHERE manga_id = %s', (manga_id,))
        return cur.fetchall()


def reorder(ids):
    id_key_pairs = list(enumerate(ids))
    with conn.cursor() as cur:
        try:
            cur.executemany(
                'UPDATE chapters SET (sort_key)=(%s) WHERE chapter_id = %s',
                id_key_pairs,
            )
        except Exception as e:
            conn.rollback()
            raise e

    conn.commit()
