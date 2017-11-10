from copy import deepcopy
import json

import cerberus
import flask


def standard_request(
        params=None,
        validator=None,
        db_call=None,
        formatter=None,
):

    if validator:
        v = cerberus.Validator(schema=validator)
        if v.validate(strip_none(params)):
            validated_params = v.document
        else:
            return make_response({
                'status': 'validation error',
                'err_message': v.errors
            }, code=400)
    else:
        validated_params = deepcopy(params)

    if db_call:
        try:
            results = db_call(**validated_params)
        except Exception as e:
            return make_response({
                'status': 'database error',
                'err_message': str(e)
            }, code=500)
    else:
        results = deepcopy(validated_params)

    if formatter:
        try:
            results = formatter(results, validated_params)
        except Exception as e:
            return make_response({
                'status': 'formatter error',
                'err_message': str(e)
            }, code=500)
    else:
        pass

    return make_response({
        'status': 'success',
        'data': results
    }, code=200)


def make_response(data, code=200):
    response = flask.Response()
    response.headers.set('Content-Type', 'application/json')
    response.status_code = code
    response.set_data(json.dumps(data, default=fmt_json))
    return response


def fmt_json(obj):
    if type(obj).__name__ == 'datetime':
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    raise TypeError(
        'You tried to json dump an unserializable type, and should implement it in standard_request.py\n' +
        'Type: {obj_type}\n'.format(obj_type=str(type(obj))) +
        'Name: {name}'.format(name=type(obj).__name__)
    )


def strip_none(arg):
    return {key: val for key, val in arg.items() if val is not None}
