
import sys
from pathlib import Path
import subprocess

from config import FFMPEG_PATH


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
    subprocess.run(cmd, check=True)


def main():
    stream_dir = Path("stream")
    generate_hls(
        Path(r"D:\Music\OriginalMusic\BattleTheme7_loop.wav"),
        stream_dir / Path("playlist.m3u8"),
        stream_dir / Path("audio%03d.aac"))

    return 0


if __name__ == "__main__":
    sys.exit(main())

