from flask import request
import logging

import backend
from common import render_template
from security import authenticated

logger = logging.getLogger(__name__)


@authenticated
def file_route_index(api_key):
    logger.info('Responding to file::error')
    files = backend.file.index()
    return render_template('file_index', files=files)
