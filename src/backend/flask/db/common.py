import psycopg2

from secret import postgres_password


class SqlArgumentError(Exception):
    pass


conn = psycopg2.connect('dbname=homulili user=homulili host=127.0.0.1 password={postgres_password}'.format(
    postgres_password=postgres_password,
))


def update_not_null(table_name, args, condition):
    if not args:
        return

    args = {key: value for key, value in args.items() if value is not None}

    keys = list(args.keys())
    keys.sort()
    values = [args[key] for key in keys]

    sql = 'UPDATE {table} SET '.format(table=table_name)
    sql = sql + ', '.join(['{key} = %s'.format(key=key) for key in keys])
    sql = sql + ' WHERE {col} = %s'.format(col=condition[0])

    results = None

    with conn.cursor() as cur:
        if args:
            try:
                cur.execute(sql, values + [condition[1]])
            except Exception as e:
                conn.rollback()
                raise e

        cur.execute(
            'SELECT * FROM {table} WHERE {col} = %s'.format(
                table=table_name,
                col=condition[0],
            ),
            (condition[1],),
        )
        results = cur.fetchone()

    conn.commit()
    return results
