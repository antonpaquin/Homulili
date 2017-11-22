import fs.osfs
import jinja2
import logging

logger = logging.getLogger(__name__)

templates = fs.osfs.OSFS('templates')
js = fs.osfs.OSFS('js')
css = fs.osfs.OSFS('css')
lib = fs.osfs.OSFS('lib')


def render_template(name, **kwargs):
    filename = '/{name}.html.j2'.format(name=name)
    if templates.isfile(filename):
        with templates.open(filename, 'r') as template_f:
            template = jinja2.Template(template_f.read())
            html = template.render(**kwargs)
        return html
    else:
        logger.warning('Request for missing resource: {name}'.format(
            name=filename,
        ))
        return ''


def render_scss(name):
    filename = '/{name}.css'.format(name=name)
    if css.isfile(filename):
        with css.open(filename, 'r') as css_f:
            return css_f.read()
            # return scss.parser.parse(scss_f.read())
    else:
        logger.warning('Request for missing resource: {name}'.format(
            name=filename,
        ))
        return ''


def render_js(name):
    filename = '/{name}.js'.format(name=name)
    if js.isfile(filename):
        with js.open(filename, 'r') as js_f:
            return js_f.read()
    else:
        logger.warning('Request for missing resource: {name}'.format(
            name=filename,
        ))
        return ''


def render_lib(name):
    filename = '/{name}'.format(name=name)
    if lib.isfile(filename):
        with lib.open(filename, 'r') as lib_f:
            return lib_f.read()
    else:
        logger.warning('Request for missing resource: {name}'.format(
            name=filename,
        ))
        return ''


def render_bin(name):
    filename = '/{name}'.format(name=name)
    if lib.isfile(filename):
        with lib.open(filename, 'rb') as lib_f:
            return lib_f.read()
    else:
        logger.warning('Request for missing resource: {name}'.format(
            name=filename,
        ))
        return ''
