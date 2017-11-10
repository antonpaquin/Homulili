from . import common


__manga_name = {
    'required': False,
    'type': 'string',
    'minlength': 1,
    'maxlength': 255,
}
__manga_name_required = common.required(__manga_name)

__author = {
    'required': False,
    'type': 'string',
    'maxlength': 255,
}

__madokami_regex = 'https:\/\/manga\.madokami\.al\/.*'
__madokami_link = {
    'required': False,
    'type': 'string',
    'regex': __madokami_regex,
}
__madokami_link_required = common.required(__madokami_link)

__active = {
    'required': False,
    'nullable': True,
    'type': 'boolean',
    'coerce': common.guess_bool,
}

__manga_id = {
    'required': False,
    'type': 'integer',
    'coerce': int,
    'min': 0,
}
__manga_id_required = common.required(__manga_id)

create = {
    'manga_name': __manga_name_required,
    'author': __author,
    'madokami_link': __madokami_link,
    'active': __active,
}

read = {
    'manga_id': __manga_id_required,
}

update = {
    'manga_id': __manga_id_required,
    'manga_name': __manga_name,
    'author': __author,
    'madokami_link': __madokami_link,
    'active': __active,
}

delete = {
    'manga_id': __manga_id_required,
}

index = {
}
