import json

from dataflow.utils import input_protection

from .common import File, Chapter, Page


@input_protection()
def printer(input):
    if isinstance(input, File):
        print(json.dumps({
            'manga_id': input.manga_id,
            'location': input.location,
            'file_id': input.file_id,
        }, indent=4))

    elif isinstance(input, Chapter):
        print(json.dumps({
            'manga_id': input.manga_id,
            'chapter_name': input.name,
            'sort_key': input.sort_key,
        }, indent=4))

    elif isinstance(input, Page):
        print(json.dumps({
            'sort_key': input.sort_key,
            'chapter': str(input.chapter),
            'file_id': input.file_id,
            'data-len': len(input.data),
        }, indent=4))

    else:
        print(input)

    print("\n###############\n")
