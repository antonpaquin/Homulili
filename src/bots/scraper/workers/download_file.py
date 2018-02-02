from queue import Queue
import requests
from requests.auth import HTTPBasicAuth
from fs.osfs import OSFS
import fs.path
import logging

from dataflow.utils import input_protection
import backend
import secret
import config

from .common import File

logger = logging.getLogger(__name__)


madokami_auth = HTTPBasicAuth(secret.madokami_uname, secret.madokami_pass)
# noinspection PyUnresolvedReferences
pyfs = OSFS(config.storage_dir)


@input_protection()
def download_file(input: File, output: Queue):
    try:
        logger.debug('Entering download_file')
        subdir = fs.path.join(*fs.path.split(input.location)[:-1])
        if not pyfs.isdir(subdir):
            pyfs.makedirs(subdir)

        logger.info('Starting download for {manga_id}: {name}'.format(
            manga_id=input.manga_id,
            name=input.location,
        ))
        data = requests.get(url=input.url, auth=madokami_auth, stream=True)
        with pyfs.open(input.location, 'wb') as data_f:
            for block in data.iter_content(1024):
                data_f.write(block)
        logger.info('Download complete')

        output.put(input)

    except Exception as e:
        logger.error('Download failed for {manga_id}: {name}, err: {err}'.format(
            manga_id=input.manga_id,
            name=input.location,
            err=str(e),
        ))
        backend.file.update(file_id=input.file_id, state='error')
