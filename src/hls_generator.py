
from pathlib import Path
import subprocess
from logging import getLogger
import traceback

from config import FFMPEG_PATH, AAC_BITRATE, HLS_LENGTH, AAC_ENCODER
from util import decode_subprocess_stream


def generate_hls(
        input_audio_path: Path,
        output_m3u8_path: Path,
        output_audio_path: Path) -> None:

    logger = getLogger(__name__)

    cmd = "\"{}\" -i \"{}\" -acodec {} -ab {} -f hls -hls_time {} -hls_playlist_type vod -hls_segment_filename \"{}\" \"{}\""
    cmd = cmd.format(
        FFMPEG_PATH,
        input_audio_path,
        AAC_ENCODER,
        AAC_BITRATE,
        HLS_LENGTH,
        output_audio_path,
        output_m3u8_path)

    logger.debug("ffmpeg command={}".format(cmd))

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    except FileNotFoundError as e:
        logger.info("Not found ffmpeg: {}. Please copy ffmpeg program to src folder.".format(FFMPEG_PATH))
        raise

    logger.debug("ffmpeg stdout={}".format(decode_subprocess_stream(proc.stdout)))
    logger.debug("ffmpeg stderr={}".format(decode_subprocess_stream(proc.stderr)))
    logger.debug("ffmpeg returncode={}".format(proc.returncode))

    proc.check_returncode()


