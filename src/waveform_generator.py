
from typing import Tuple
import sys
from pathlib import Path
import subprocess
import wave
import io
import random
import string

import numpy as np
from PIL import Image, ImageChops

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

from config import FFMPEG_PATH


def _convert_to_wav_for_vis(input_wave: Path) -> bytes:
    cmd = "\"{}\" -i \"{}\" -ac 1 -ar 8000 -acodec pcm_s16le -f wav -"
    cmd = cmd.format(FFMPEG_PATH, input_wave)
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True)
    return proc.stdout


def _wav_to_ndarray(wav_bytes: bytes) -> np.ndarray:
    with wave.open(io.BytesIO(wav_bytes)) as f:
        return np.frombuffer(f.readframes(-1), dtype=np.int16).astype(dtype=np.float32)


def _downsample(array: np.ndarray, width: int, height: int) -> np.ndarray:
    splited = np.array_split(array, width)
    downsampled = np.asarray(
        [(splited_elem[0] / (2**15)) * height for splited_elem in splited],
        dtype=np.float32)
    return downsampled


def _draw_graph(
        array: np.ndarray,
        graph_path: Path,
        size: Tuple[int, int]) -> None:

    plt.figure(figsize=size, dpi=100)
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_ylim([-256, 256])
    plt.plot(array, linewidth=0.5, color="white")
    plt.autoscale(axis="x", tight=True)
    plt.savefig(graph_path, transparent=True)


def _colorize_graph(
        graph_img_path: Path,
        colorized_img_path: Path,
        color: Tuple[int, int, int]) -> None:

    graph_img = Image.open(graph_img_path)
    color_img = Image.new("RGBA", graph_img.size, (*color, 255))
    ImageChops.multiply(graph_img, color_img).save(colorized_img_path)


def _generate_temp_filename() -> str:
    return "".join([random.choice(string.digits) for _ in range(10)])


def generate_waveform_graph(
        wav_path: Path,
        playing_waveform_path: Path,
        playing_waveform_color: Tuple[int, int, int],
        played_waveform_path: Path,
        played_waveform_color: Tuple[int, int, int]) -> None:

    temp_waveform_path = Path(_generate_temp_filename() + ".png")

    try:
        wav_bytes = _convert_to_wav_for_vis(wav_path)
        wav_array = _wav_to_ndarray(wav_bytes)
        wav_array = _downsample(wav_array, 50000, 256)
        _draw_graph(wav_array, temp_waveform_path, (6, 1))

        _colorize_graph(
            temp_waveform_path,
            playing_waveform_path,
            playing_waveform_color)

        _colorize_graph(
            temp_waveform_path,
            played_waveform_path,
            played_waveform_color)

    except:
        raise
    finally:
        temp_waveform_path.unlink()

