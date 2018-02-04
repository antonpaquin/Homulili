from flask import Flask
import logging

from common import render_template, render_scss, render_js, render_lib, render_bin

import security
import manga
import chapter
import page
import pagedata
import file

import config


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-24s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/var/log/homulili/frontend.log',
    filemode='w',
)
logger = logging.getLogger('route')


app = Flask(__name__)

app.route('/login')(security.login)
app.route('/login/create_target', methods=['POST'])(security.create_target)
app.route('/login/login_target', methods=['POST'])(security.login_target)

app.route('/manga')(manga.manga_route_index)
app.route('/manga/create_target')(manga.manga_route_create_target)
app.route('/manga/rename_target')(manga.manga_route_rename_target)
app.route('/manga/delete_target')(manga.manga_route_delete_target)

app.route('/chapter/index')(chapter.chapter_route_index)
app.route('/chapter/rename_target')(chapter.chapter_route_rename_target)
app.route('/chapter/resort_target')(chapter.chapter_route_resort_target)
app.route('/chapter/delete_target')(chapter.chapter_route_delete_target)

app.route('/page/display')(page.page_route_display)
app.route('/page/rechapter_target', methods=['POST'])(page.page_route_rechapter_target)

app.route('/pagedata/display')(pagedata.pagedata_route_display)

app.route('/file')(file.file_route_index)


@app.route('/')
def root():
    return render_template('root')


@app.route('/css/<src>')
def route_css(src):
    return render_scss(src)


@app.route('/js/<src>')
def route_js(src):
    return render_js(src)


@app.route('/lib/<src>')
def route_lib(src):
    return render_lib(src)


@app.route('/lib/images/<src>')
def route_lib_images(src):
    return render_bin('images/' + src)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config.admin_internal_port))
