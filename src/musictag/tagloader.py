
from typing import NamedTuple
import traceback
from logging import getLogger

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

        tagloader_exceptions = []

        for loader in loader_funcs:
            try:
                return MusicMetadata(**loader(file_path))
            except TagLoaderException:
                tagloader_exceptions.append(traceback.format_exc())

        # 全部のタグローダが失敗した場合は，すべての例外をログに残す
        MusicMetadata._log_exceptions(loader_funcs, tagloader_exceptions)

        raise TagLoaderException("Failed to load tag.")

    @staticmethod
    def _log_exceptions(loader_funcs, exceptions):
        logger = getLogger(__name__)
        logger.error("All tagloader is failed.")

        for loader, ex in zip(loader_funcs, exceptions):
            loader_name = loader.__module__ + "." + loader.__name__
            message = "Exception in {}\n{}".format(loader_name, ex)
            logger.error(message)
