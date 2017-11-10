from .common import required

__page_id = {
    'required': False,
    'type': 'integer',
    'coerce': int,
}
__page_id_required = required(__page_id)


__data = {
    'required': False,
}
__data_required = required(__data)


create = {
    'page_id': __page_id_required,
    'data': __data_required,
}


read = {
    'page_id': __page_id_required,
}


delete = {
    'page_id': __page_id_required,
}
