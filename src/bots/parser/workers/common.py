class File:
    def __init__(self, manga_id, location, file_id):
        self.manga_id = manga_id
        self.location = location
        self.file_id = file_id


class Chapter:
    def __init__(self, manga_id, name, sort_key):
        self.manga_id = manga_id
        self.name = name
        self.sort_key = sort_key

        self.chapter_id = None

class Page:
    def __init__(self, chapter, sort_key, file_id, data):
        self.sort_key = sort_key
        self.file_id = file_id
        self.chapter = chapter
        self.data = data

        self.page_id = None
