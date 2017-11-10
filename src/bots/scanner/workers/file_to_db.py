import flask_interface
from dataflow.utils import input_protection
from workers.newfile_filter import NewFile


@input_protection()
def file_to_db(input: NewFile):
    print('Add new file for manga {manga_id}: {url}'.format(
        manga_id=input.manga_id,
        url=input.url,
    ))

    flask_interface.file.create(
        manga_id=input.manga_id,
        file_url=input.url,
        location=input.location,
        downloaded=input.downloaded,
        ignore=input.ignore,
    )
