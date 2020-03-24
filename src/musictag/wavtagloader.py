
import os
from typing import Dict
from logging import getLogger

from .wavchunkloader import \
    WavefileChunk, WavefileFmt, find_chunk, parse_info_chunk
from .util import TagLoaderException, get_or_default, bytes2str


def load(file_path) -> Dict[str, str]:
    with open(file_path, "rb") as f:
        wavchunk = WavefileChunk.read_from(f)

    riff_chunk = find_chunk(wavchunk, name=b"RIFF", typename=b"WAVE")
    if riff_chunk is None:
        raise TagLoaderException("Not found WAVE chunk.")

    data_chunk = find_chunk(wavchunk, name=b"data")

    fmt_chunk = find_chunk(wavchunk, name=b"fmt ")
    fmt = WavefileFmt.unpack(fmt_chunk.data)

    info_chunk = find_chunk(wavchunk, name=b"LIST", typename=b"INFO")
    if info_chunk is None:
        # INFOチャンクが無かった場合は，タイトルをファイル名で代用する
        filename = os.path.splitext(os.path.basename(str(file_path)))[0]

        info_message = (
            "Fallbacking to title is filename, " +
            "because INFO chunk is not found in soundfile \"{}\"")
        info_message = info_message.format(filename)
        getLogger(__name__).info(info_message)

        return {
            "title": filename,
            "artist": "",
            "album": "",
            "year": "",
            "duration": data_chunk.size / fmt.bytespersec
        }
    else:
        info_dict = parse_info_chunk(info_chunk)
        return {
            "title": get_or_default(info_dict, "INAM"),
            "artist": get_or_default(info_dict, "IART"),
            "album": get_or_default(info_dict, "IPRD"),
            "year": int(get_or_default(info_dict, "ICRD", 0)),
            "duration": data_chunk.size / fmt.bytespersec
        }

