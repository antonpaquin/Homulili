from . import common
from .chapter import __chapter_id, __chapter_id_required


__page_id = {
    'required': False,
    'type': 'integer',
    'min': 0,
    'coerce': int,
}
__page_id_required = common.required(__page_id)


__sort_key = {
    'required': False,
    'type': 'integer',
    'coerce': int,
}

__file_name = {
    'required': False,
    'type': 'string',
    'minlength': 1,
}

__file_id = {
    'required': False,
    'type': 'integer',
    'coerce': int,
    'min': 0,
}


create = {
    'chapter_id': __chapter_id_required,
    'sort_key': __sort_key,
    'file_id': __file_id,
}


read = {
    'page_id': __page_id_required,
}


update = {
    'page_id': __page_id_required,
    'chapter_id': __chapter_id,
    'sort_key': __sort_key,
    'file_name': __file_name,
}


delete = {
    'page_id': __page_id_required,
}


index = {
    'chapter_id': __chapter_id_required,
}
