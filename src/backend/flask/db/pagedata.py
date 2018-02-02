from .common import conn


def create(page_id, data):
    with conn.cursor() as cur:
        cur.execute('INSERT INTO pagedata(page_id, data) VALUES (%s, %s)', (page_id, data))

    conn.commit()


def read(page_id):
    with conn.cursor() as cur:
        cur.execute('SELECT data FROM pagedata WHERE page_id=%s', (page_id,))
        return cur.fetchone()


def delete(page_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM pagedata WHERE page_id=%s', (page_id,))

    conn.commit()
