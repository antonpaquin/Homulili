from flask import request, Response

import backend
from security import authenticated


@authenticated
def pagedata_route_display():
    if 'page_id' not in request.args:
        return '', 400

    page_id = request.args.get('page_id')

    response = Response()
    response.set_data(backend.pagedata.read(page_id))
    response.headers.set('Content-Type', 'image/png')
    response.status_code = 200
    return response
