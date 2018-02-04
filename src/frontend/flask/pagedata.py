from flask import request, Response
import logging

import backend
from security import authenticated

logger = logging.getLogger(__name__)


@authenticated
def pagedata_route_display(api_key):
    logger.info('Responding to pagedata::display')
    if 'page_id' not in request.args:
        logger.warning('No page_id in request')
        return '', 400

    page_id = request.args.get('page_id')

    response = Response()
    response.set_data(backend.pagedata.read(page_id))
    response.headers.set('Content-Type', 'image/png')
    response.status_code = 200
    return response
