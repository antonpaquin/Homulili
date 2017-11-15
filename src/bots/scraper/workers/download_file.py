from queue import Queue
import requests
from requests.auth import HTTPBasicAuth
from fs.osfs import OSFS
import fs.path

from dataflow.utils import input_protection
import backend
import secret
import config

from .common import File


madokami_auth = HTTPBasicAuth(secret.madokami_uname, secret.madokami_pass)
# noinspection PyUnresolvedReferences
pyfs = OSFS(config.storage_dir)


@input_protection()
def download_file(input: File, output: Queue):
    subdir = fs.path.join(*fs.path.split(input.location)[:-1])
    if not pyfs.isdir(subdir):
        pyfs.makedirs(subdir)

    # Before running a download, run a final check to see if we actually need the file
    pre_check = backend.file.read(input.file_id)
    if pre_check['ignore'] or pre_check['downloaded']:
        return

    print('Starting download for {manga_id}: {name}'.format(
        manga_id=input.manga_id,
        name=input.location,
    ))
    data = requests.get(url=input.url, auth=madokami_auth, stream=True)
    with pyfs.open(input.location, 'wb') as data_f:
        for block in data.iter_content(1024):
            data_f.write(block)
    print('Download complete')

    input.downloaded = True

    output.put(input)
