from .common import conn, update_not_null


# noinspection PyUnboundLocalVariable
def create(chapter_id, sort_key=0, file_id=None):
    with conn.cursor() as cur:
        try:
            cur.execute(
                'INSERT INTO pages (chapter_id, sort_key, file_id) VALUES (%s, %s, %s)',
                (chapter_id, sort_key, file_id),
            )
        except Exception as e:
            conn.rollback()
            raise e

        cur.execute('SELECT currval(\'pages_page_id_seq\')')
        new_id = cur.fetchone()

    conn.commit()
    return new_id


def read(page_id):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM pages WHERE page_id = %s', (page_id,))
        return cur.fetchone()


def update(page_id, chapter_id=None, sort_key=None, file_name=None):
    return update_not_null(
        table_name='pages',
        args={
            'chapter_id': chapter_id,
            'sort_key': sort_key,
            'file_name': file_name,
        },
        condition=('page_id', page_id),
    )


def delete(page_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM pages WHERE page_id = %s', (page_id,))

    conn.commit()


def index(chapter_id):
    with conn.cursor() as cur:
        cur.execute('SELECT page_id, sort_key FROM pages WHERE chapter_id = %s', (chapter_id,))
        return cur.fetchall()
