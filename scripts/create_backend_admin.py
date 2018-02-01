import psycopg2
import random

from secret import postgres_password


key = ''.join([
    random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    for _ in range(30)
])

conn = psycopg2.connect('dbname=homulili user=homulili host=127.0.0.1 password={postgres_password}'.format(
    postgres_password=postgres_password,
))

with conn.cursor() as cur:
    try:
        cur.execute(
            'INSERT INTO api_access (api_key, p_create, p_read, p_update, p_delete, p_index, p_command, p_admin)'
            'VALUES (%s, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE)',
            (key,),
        )
    except Exception as e:
        conn.rollback()
        raise e

    conn.commit()

print('Admin key: {key}'.format(
    key=key,
))
