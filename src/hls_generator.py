
from pathlib import Path
import subprocess
from logging import getLogger

from config import FFMPEG_PATH
from util import decode_subprocess_stream


def generate_hls(
        input_audio_path: Path,
        output_m3u8_path: Path,
        output_audio_path: Path) -> None:

    cmd = "\"{}\" -i \"{}\" -acodec aac -f hls -hls_time {} -hls_playlist_type vod -hls_segment_filename \"{}\" \"{}\""
    cmd = cmd.format(
        FFMPEG_PATH,
        input_audio_path,
        4,
        output_audio_path,
        output_m3u8_path)

    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    logger = getLogger(__name__)
    logger.debug("ffmpeg stdout={}".format(decode_subprocess_stream(proc.stdout)))
    logger.debug("ffmpeg stderr={}".format(decode_subprocess_stream(proc.stderr)))
    logger.debug("ffmpeg returncode={}".format(proc.returncode))

    proc.check_returncode()


