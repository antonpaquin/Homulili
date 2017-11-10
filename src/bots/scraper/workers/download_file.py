from queue import Queue
import requests
from requests.auth import HTTPBasicAuth
from fs.osfs import OSFS
import fs.path

from dataflow.utils import input_protection
import flask_interface
import secret
import config

from .common import File


madokami_auth = HTTPBasicAuth(*secret.madokami_auth)
# noinspection PyUnresolvedReferences
pyfs = OSFS(config.pyfs_container)


@input_protection()
def download_file(input: File, output: Queue):
    print('Enter download_file')
    subdir = fs.path.join(*fs.path.split(input.location)[:-1])
    if not pyfs.isdir(subdir):
        pyfs.makedirs(subdir)

    # Before running a download, run a final check to see if we actually need the file
    pre_check = flask_interface.file.read(input.file_id)
    if pre_check['ignore'] or pre_check['downloaded']:
        return

    data = requests.get(url=input.url, auth=madokami_auth)
    print('Downloaded file for {manga_id}: {name}'.format(
        manga_id=input.manga_id,
        name=input.location,
    ))

    with pyfs.open(input.location, 'wb') as data_f:
        data_f.write(data.content)

    input.downloaded = True

    output.put(input)
