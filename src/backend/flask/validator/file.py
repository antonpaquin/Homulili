from . import common
from .manga import __manga_id, __manga_id_required


__url = {
    'required': False,
    'type': 'string',
    'regex': common.url_regex,
}
__url_required = common.required(__url)


__location = {
    'required': False,
    'type': 'string',
}
__location_required = common.required(__location)

__state = {
    'required': False,
    'type': 'string',
    'allowed': ['ready', 'downloading', 'downloaded', 'parsing', 'done', 'error', 'ignore'],
}
__state_required = common.required(__state)

__file_id = {
    'required': False,
    'type': 'integer',
    'coerce': int,
    'min': 0,
}
__file_id_required = common.required(__file_id)


create = {
    'manga_id': __manga_id_required,
    'url': __url_required,
    'location': __location,
    'state': __state,
}


read = {
    'file_id': __file_id_required,
}


update = {
    'file_id': __file_id_required,
    'manga_id': __manga_id,
    'url': __url,
    'location': __location,
    'state': __state,
}


delete = {
    'file_id': __file_id_required,
}


index = {
    'manga_id': __manga_id,
    'state': __state,
}
