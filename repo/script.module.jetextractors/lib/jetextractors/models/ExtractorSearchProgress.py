from .Extractor import Extractor
import typing

class ExtractorSearchProgress:
    done: int
    total: int
    links: int
    cancelled: bool
    extractors: typing.List

    def __init__(self,) -> None:
        self.done = 0
        self.total = -1
        self.links = 0
        self.cancelled = False
        self.extractors = []
