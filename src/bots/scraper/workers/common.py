class File:
    def __init__(self, file_id: int, manga_id: int, url: str, location: str,
                 downloaded: bool, ignore: bool, parsed: bool):
        self.file_id = file_id
        self.manga_id = manga_id
        self.url = url
        self.location = location
        self.downloaded = downloaded
        self.ignore = ignore
        self.parsed = parsed
