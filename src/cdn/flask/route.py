import flask
import logging

import cerberus
import psycopg2

import secret
import config

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-24s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/var/log/homulili/frontend.log',
    filemode='w',
)
logger = logging.getLogger('route')


conn = psycopg2.connect('dbname=homulili_cdn user=homulili host=127.0.0.1 password={postgres_password}'.format(
    postgres_password=secret.postgres_password,
))


app = flask.Flask(__name__)


@app.route('/<img_id>')
def image(img_id):
    with conn.cursor() as cur:
        cur.execute('SELECT data FROM imgdata WHERE img_id=%s', (img_id,))
        results = cur.fetchone()

    response = flask.Response()

    if results:
        response.set_data(bytes(results[0]))
        response.status_code = 200
        response.headers.set('Content-Type', 'image/png')
    else:
        response.set_data(bytes(0))
        response.status_code = 404

    return response


@app.route('/upload', methods=['POST'])
def upload():
    with conn.cursor() as cur:
        cur.execute('INSERT INTO imgdata(data) VALUES (%s)', (flask.request.data,))
        cur.execute('SELECT currval(\'imgdata_img_id_seq\')')
        new_id = cur.fetchone()[0]
    conn.commit()
    return flask.jsonify(new_id=new_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config.cdn_internal_port))
