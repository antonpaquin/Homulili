from . import common

__permission = {
    'required': False,
    'type': 'boolean',
    'coerce': common.guess_bool,
}
__permission_required = common.required(__permission)

__api_key = {
    'required': False,
    'type': 'string',
}
__api_key_required = common.required(__api_key)

create = {
    'create': __permission,
    'read': __permission,
    'update': __permission,
    'delete': __permission,
    'index': __permission,
    'command': __permission,
    'admin': __permission,
}

read = {
    'api_key': __api_key_required,
}

update = {
    'api_key': __api_key_required,
    'create': __permission,
    'read': __permission,
    'update': __permission,
    'delete': __permission,
    'index': __permission,
    'command': __permission,
    'admin': __permission,
}

delete = {
    'api_key': __api_key_required,
}
