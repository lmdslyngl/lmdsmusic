
from typing import List, Tuple
from pathlib import Path
import sys
import logging
from datetime import datetime

from config import DATA_DIR


class SiteGeneratorException(Exception):
    pass


def decode_subprocess_stream(stream: bytes) -> str:
    return stream.decode("cp932", errors="ignore").replace("\r\n", "\n")


def replace_content(path: Path, replace_texts: List[Tuple[str, str]]):
    """ ファイル内の特定の文字列を置換する """

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    for before, after in replace_texts:
        content = content.replace(before, after)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def is_music_file(filepath: Path) -> bool:
    music_file_extensions = [".mp3", ".wav", ".flac"]
    return filepath.suffix.lower() in music_file_extensions


def init_logger() -> logging.Logger:
    logdir = DATA_DIR / Path("log")
    if not logdir.exists():
        logdir.mkdir(parents=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

    stream_stdout = logging.StreamHandler(sys.stdout)
    stream_stdout.setFormatter(formatter)
    stream_stdout.setLevel(logging.INFO)

    logfile_name = datetime.now().strftime("%Y-%m-%dT%H-%M-%S.log")
    stream_logfile = logging.FileHandler(
        logdir / Path(logfile_name),
        encoding="utf-8")
    stream_logfile.setFormatter(formatter)
    stream_logfile.setLevel(logging.DEBUG)

    logger.addHandler(stream_stdout)
    logger.addHandler(stream_logfile)

    return logger

