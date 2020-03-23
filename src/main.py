
from typing import Tuple, List
import sys
from pathlib import Path
from hashlib import md5
import json
import toml
import shutil
from pathlib import Path
from distutils.dir_util import copy_tree
from logging import getLogger

import config
from hls_generator import generate_hls
from waveform_generator import generate_waveform_graph
from musictag.tagloader import MusicMetadata
from util import replace_content, init_logger, is_music_file


def load_siteconfig(siteconfig_path: Path) -> dict:
    with open(siteconfig_path, encoding="utf-8") as f:
        return toml.load(f)


def generate_site(
        site_template_dir: Path,
        siteconfig: dict,
        output_site_dir: Path):

    copy_tree(str(site_template_dir), str(output_site_dir))

    replace_texts = [
        ("${title}", siteconfig["title"]),
        ("${profile_thumbnail}", siteconfig["profile_thumbnail"]),
        ("${profile_background}", siteconfig["profile_background"]),
        ("${username}", siteconfig["username"]),
        ("${description}", siteconfig["description"]),
        ("${copyright}", siteconfig["copyright"]),
    ]

    for document_path in output_site_dir.glob("*.html"):
        replace_content(document_path, replace_texts)


def generate_streams(
        source_dir: Path,
        musicinfo_list: List[dict],
        output_streams_dir: Path) -> None:

    if not output_streams_dir.exists():
        output_streams_dir.mkdir(parents=True)

    for source in source_dir.glob("*.*"):
        if not is_music_file(source):
            continue

        getLogger(__name__).info("Generating streams: {}".format(source))

        audio_id = md5(source.name.encode("utf-8")).hexdigest()

        stream_dir = output_streams_dir / Path(audio_id)
        if not stream_dir.exists():
            # ストリー見ディレクトリが無かったときはストリームを生成する
            stream_dir.mkdir()

            generate_hls(
                source,
                stream_dir / Path("playlist.m3u8"),
                stream_dir / Path("audio%03d.aac"))

            generate_waveform_graph(
                source,
                stream_dir / Path("waveform_playing.png"),
                (230, 230, 230),
                stream_dir / Path("waveform_played.png"),
                (28, 32, 80))

        # ストリームディレクトリがあってもmusicinfoの更新は常に行う
        try:
            musicinfo = next(filter(
                lambda x: x["id"] == audio_id,
                musicinfo_list))
        except StopIteration:
            musicinfo = None

        musicinfo["playlistUrl"] = "/stream/{}/playlist.m3u8".format(audio_id)
        musicinfo["waveformPlaying"] = "/stream/{}/waveform_playing.png".format(audio_id)
        musicinfo["waveformPlayed"] = "/stream/{}/waveform_played.png".format(audio_id)

        with open(stream_dir / Path("musicinfo.json"), "w") as f:
            json.dump(musicinfo, f)


def generate_music_list(
        musicinfo_list: List[dict],
        output_music_list_path: Path) -> None:

    music_list = []
    for musicinfo in musicinfo_list:
        music_list.append((
            musicinfo["id"],
            musicinfo["title"],
            musicinfo["last_modified"]))

    with open(output_music_list_path, "w") as f:
        json.dump(music_list, f)


def delete_unused_streams(
        musicinfo_list: List[dict],
        streams_dir: Path) -> None:

    used_ids = {musicinfo["id"] for musicinfo in musicinfo_list}
    for stream_dir in streams_dir.glob("*"):
        if stream_dir.is_dir() and stream_dir.name not in used_ids:
            shutil.rmtree(stream_dir)


def generate_musicinfo_list(
        source_dir: Path,
        default_music_thumbnail: str,
        musicinfo_list_path: Path) -> List[dict]:

    try:
        with open(config.DATA_DIR / Path("musicinfo_list.toml"), "r", encoding="utf-8") as f:
            musicinfo_list = toml.load(f)["musicinfo_list"]
    except FileNotFoundError:
        musicinfo_list = []

    # musicinfo_listに入ってるID
    musicinfo_ids = {musicinfo["id"] for musicinfo in musicinfo_list}

    # sourceディレクトリに入ってる曲のID
    source_ids = set()

    for source in config.SOURCE_DIR.glob("*.*"):
        if not is_music_file(source):
            continue

        audio_id = md5(source.name.encode("utf-8")).hexdigest()
        source_ids.add(audio_id)

        if audio_id in musicinfo_ids:
            # すでにmusicinfo_listにあるときは無視
            continue

        # musicinfo_listに無い曲だけ末尾に追加
        metadata = MusicMetadata.read(source)
        last_modified_time = source.stat().st_mtime
        musicinfo_list.append({
            "id": audio_id,
            "title": metadata.title,
            "artist": metadata.artist,
            "album": metadata.album,
            "duration": metadata.duration,
            "last_modified": last_modified_time,
            "thumbnail": default_music_thumbnail
        })

    # sourceディレクトリに入っている曲のみを残す
    musicinfo_list = list(filter(
        lambda x: x["id"] in source_ids,
        musicinfo_list))

    with open(config.DATA_DIR / Path("musicinfo_list.toml"), "w", encoding="utf-8") as f:
        toml.dump({"musicinfo_list": musicinfo_list}, f)

    return musicinfo_list


def main():
    init_logger()
    logger = getLogger(__name__)
    logger.info("Started site generator script.")

    try:
        siteconfig = load_siteconfig(config.DATA_DIR / Path("siteconfig.toml"))

        logger.info("Generating musicinfo list")
        musicinfo_list = generate_musicinfo_list(
            config.SOURCE_DIR,
            siteconfig["default_music_thumbnail"],
            config.DATA_DIR / Path("musicinfo_list.toml"))

        logger.info("Generating streams")
        generate_streams(
            config.SOURCE_DIR,
            musicinfo_list,
            config.STREAM_DIR)

        logger.info("Generating musiclist")
        generate_music_list(
            musicinfo_list,
            config.STREAM_DIR / Path("musiclist.json"))

        logger.info("Deleting unused streams")
        delete_unused_streams(
            musicinfo_list,
            config.STREAM_DIR)

        logger.info("Generating site")
        generate_site(
            config.SITE_TEMPLATE_DIR,
            siteconfig,
            config.GENERATED_SITE_DIR)

    except Exception as e:
        logger.exception(e)

    logger.info("Finished site generator script.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
