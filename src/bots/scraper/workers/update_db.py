from dataflow.utils import input_protection
import backend

from .common import File


@input_protection()
def update_db(input: File):
    backend.file.update(
        file_id=input.file_id,
        manga_id=input.manga_id,
        file_url=input.url,
        location=input.location,
        downloaded=input.downloaded,
        ignore=input.ignore,
        parsed=input.parsed,
    )
