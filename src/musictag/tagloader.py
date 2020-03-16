
from typing import NamedTuple
import traceback

from . import mutagentagloader
from . import wavtagloader
from .util import TagLoaderException


class MusicMetadata(NamedTuple):
    title: str
    artist: str
    album: str
    year: int
    duration: float

    @staticmethod
    def read(file_path) -> "MusicMetadata":
        loader_funcs = [
            mutagentagloader.load,
            wavtagloader.load
        ]

        for loader in loader_funcs:
            try:
                return MusicMetadata(**loader(file_path))
            except TagLoaderException:
                pass

        raise TagLoaderException("Failed to load tag.")
