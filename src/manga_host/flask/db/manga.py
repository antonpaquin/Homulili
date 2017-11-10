from .common import conn, update_not_null


def create(manga_name='MISSING NAME', author='MISSING_AUTHOR',
           madokami_link='https://manga.madokami.al/404', active=True):
    with conn.cursor() as cur:
        try:
            cur.execute(
                'INSERT INTO manga (manga_name, author, madokami_link, active) VALUES (%s, %s, %s, %s)',
                (manga_name, author, madokami_link, active)
            )
        except Exception as e:
            conn.rollback()
            raise e

        cur.execute('SELECT currval(\'manga_manga_id_seq\')')
        new_id = cur.fetchone()

    conn.commit()
    # noinspection PyUnboundLocalVariable
    return new_id


def read(manga_id):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM manga WHERE manga_id = %s', (manga_id,))
        return cur.fetchone()


def update(manga_id, manga_name=None, author=None, madokami_link=None, active=None):
    return update_not_null(
        table_name='manga',
        args={
            'manga_name': manga_name,
            'author': author,
            'madokami_link': madokami_link,
            'active': active,
        },
        condition=('manga_id', manga_id),
    )


def delete(manga_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM manga WHERE manga_id = %s', (manga_id,))

    conn.commit()


def index():
    with conn.cursor() as cur:
        cur.execute('SELECT manga_id, manga_name FROM manga')
        return cur.fetchall()
