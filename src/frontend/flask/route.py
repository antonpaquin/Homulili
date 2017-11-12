from flask import Flask

from common import render_template, render_scss, render_js, render_lib, render_bin
import manga
import chapter
import page

import config

app = Flask(__name__)


app.route('/manga')(manga.manga_route_root)
app.route('/manga/create')(manga.manga_route_create)

app.route('/chapter/index')(chapter.chapter_route_index)
app.route('/chapter/rename_target')(chapter.chapter_route_rename_target)
app.route('/chapter/reorder_target', methods=['POST'])(chapter.chapter_route_reorder_target)
app.route('/chapter/delete_target')(chapter.chapter_route_delete_target)
app.route('/chapter/resort_target')(chapter.chapter_route_resort_target)


app.route('/page/index')(page.page_route_index)
app.route('/page/display')(page.page_route_display)
app.route('/page/rechapter')(page.page_route_rechapter)
app.route('/page/rechapter_target', methods=['POST'])(page.page_route_rechapter_target)


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
    app.run(host='0.0.0.0', port=config.admin_port)
