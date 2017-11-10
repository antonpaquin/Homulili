from . import common
from .manga import __manga_id, __manga_id_required

__chapter_name = {
    'required': False,
    'type': 'string',
    'minlength': 1,
    'maxlength': 255,
}
__chapter_name_required = common.required(__chapter_name)


__chapter_id = {
    'required': False,
    'type': 'integer',
    'min': 0,
    'coerce': int,
}
__chapter_id_required = common.required(__chapter_id)


__sort_key = {
    'required': False,
    'type': 'float',
    'coerce': float,
}


create = {
    'chapter_name': __chapter_name_required,
    'manga_id': __manga_id_required,
    'sort_key': __sort_key,
}

read = {
    'chapter_id': __chapter_id_required,
}


update = {
    'chapter_id': __chapter_id_required,
    'chapter_name': __chapter_name,
    'manga_id': __manga_id,
    'sort_key': __sort_key,
}


delete = {
    'chapter_id': __chapter_id_required,
}


index = {
    'manga_id': __manga_id_required,
}

reorder = {
    'ids': {
        'type': 'list',
        'schema': __chapter_id_required
    }
}
