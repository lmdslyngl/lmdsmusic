
import sys
from pathlib import Path
import subprocess
import wave
import io
import numpy as np
import matplotlib.pyplot as plt


FFMPEG_PATH = Path("D:\\Tool\\ffmpeg-4.2.2-win64-static\\bin\\ffmpeg.exe")


def convert_to_wav_for_vis(input_wave: Path) -> bytes:
    cmd = "{} -i {} -ac 1 -ar 8000 -acodec pcm_s16le -f wav -"
    cmd = cmd.format(FFMPEG_PATH, input_wave)
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True)
    return proc.stdout


def wav_to_ndarray(wav_bytes: bytes) -> np.ndarray:
    with wave.open(io.BytesIO(wav_bytes)) as f:
        return np.frombuffer(f.readframes(-1), dtype=np.int16).astype(dtype=np.float32)


def downsample(array: np.ndarray, width: int, height: int) -> np.ndarray:
    splited = np.array_split(array, width)
    downsampled = np.asarray(
        [(splited_elem[0] / (2**15)) * height for splited_elem in splited],
        dtype=np.float32)
    return downsampled


def draw_graph(array: np.ndarray, graph_path: Path):
    plt.figure(figsize=(6, 1), dpi=100)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_ylim([-256, 256])
    plt.plot(array, linewidth=0.5, color="midnightblue")
    plt.autoscale(axis="x", tight=True)
    plt.savefig(graph_path, transparent=True)
    # plt.show()


def main():
    # wav_bytes = convert_to_wav_for_vis(
    #     Path("D:\\Music\\OriginalMusic\\BeginningVillage_loop.flac"))
    wav_bytes = convert_to_wav_for_vis(
        Path(r"D:\Music\OriginalMusic\BattleTheme7_loop.wav"))
    wav_array = wav_to_ndarray(wav_bytes)
    downsampled = downsample(wav_array, 50000, 256)
    draw_graph(downsampled, "graph.png")

    return 0


if __name__ == "__main__":
    sys.exit(main())
