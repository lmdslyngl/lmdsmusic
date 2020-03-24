
import os
from typing import Dict
from logging import getLogger
import mutagen
from mutagen.id3 import ID3
from mutagen._vorbis import VCommentDict
from mutagen.mp4 import MP4Tags
from .util import TagLoaderException, str2int, get_or_default


def load(file_path) -> Dict[str, str]:
    music_file = mutagen.File(file_path)
    if music_file is None:
        raise TagLoaderException("Unknown format media file.")

    tags = music_file.tags
    if isinstance(tags, ID3):
        tag_dict = _load_id3(tags)
    elif isinstance(tags, VCommentDict):
        tag_dict = _load_vcomment(tags)
    elif isinstance(tags, MP4Tags):
        tag_dict = _load_mp4_tags(tags)
    else:
        # タグが検出できなかったときは空文字列としておく
        tag_dict = {
            "title": "",
            "artist": "",
            "album": "",
            "year": 0
        }

    tag_dict["duration"] = music_file.info.length

    if len(tag_dict["title"]) <= 0:
        # タグにタイトルが無かったときはファイル名で代用する
        filename = os.path.splitext(os.path.basename(file_path))[0]
        tag_dict["title"] = filename

        info_message = (
            "Fallbacking to title is filename, " +
            "because failed to load tag in soundfile \"{}\"")
        info_message = info_message.format(filename)
        getLogger(__name__).info(info_message)

    return tag_dict


def _load_id3(tag: ID3) -> Dict[str, str]:
    return {
        "title": str(get_or_default(tag, "TIT2")),
        "artist": str(get_or_default(tag, "TPE1")),
        "album": str(get_or_default(tag, "TALB")),
        "year": str2int(str(get_or_default(tag, "TDRC")))
    }


def _load_vcomment(tag: VCommentDict) -> Dict[str, str]:
    return {
        "title": _join_tag_list(tag, "title"),
        "artist": _join_tag_list(tag, "artist"),
        "album": _join_tag_list(tag, "album"),
        "year": str2int(get_or_default(tag, "date", ["0"])[0])
    }


def _load_mp4_tags(tag: MP4Tags) -> Dict[str, str]:
    return {
        "title": _join_tag_list(tag, "\xa9nam"),
        "artist": _join_tag_list(tag, "\xa9ART"),
        "album": _join_tag_list(tag, "\xa9alb"),
        "year": str2int(get_or_default(tag, "\xa9day", ["0"])[0])
    }


def _join_tag_list(tag_dict, tag_name):
    tag = get_or_default(tag_dict, tag_name, [])
    return "; ".join(tag)

