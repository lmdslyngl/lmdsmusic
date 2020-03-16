
from typing import NamedTuple, List, Union, Dict, Callable, Iterable, Optional
import chunk
import struct

from .util import bytes2str


class WavefileChunk(NamedTuple):
    name: bytes
    size: int
    typename: bytes
    data: bytes
    children: List["WavefileChunk"]

    def print_recursive(self, depth=0):
        print(" " * depth, end="")
        print("name: {}, size: {}, type: {}, data: {}".format(
            self.name, self.size, self.typename, bytes2str(self.data)))
        for child in self.children:
            child.print_recursive(depth + 1)

    @staticmethod
    def read_from(wav_file) -> "WavefileChunk":
        wavchunk = WavefileChunk("DUMMY", 0, b"", b"", [])
        WavefileChunk._read_chunk_internal(wav_file, wavchunk)
        return wavchunk.children[0]

    @staticmethod
    def _read_chunk_internal(parent_chunk: chunk.Chunk, parent: "WavefileChunk"):
        try:
            while True:
                c = chunk.Chunk(parent_chunk, bigendian=False)

                if c.getname() in [b"RIFF", b"LIST"]:
                    riff_type = c.read(4)
                    wavchunk = WavefileChunk(
                        c.getname(), c.getsize(), riff_type, b"", [])

                    WavefileChunk._read_chunk_internal(c, wavchunk)

                else:
                    if c.getname() != b"data":
                        wavchunk = WavefileChunk(
                            c.getname(), c.getsize(), b"", c.read(), [])
                    else:
                        wavchunk = WavefileChunk(
                            c.getname(), c.getsize(), b"", b"", [])

                c.close()
                parent.children.append(wavchunk)

        except EOFError:
            pass


class WavefileFmt(NamedTuple):
    wave_format: int
    channels: int
    samplerate: int
    bytespersec: int
    blockalign: int
    bitswidth: int

    @staticmethod
    def unpack(buffer: bytes) -> "WavefileFmt":
        return WavefileFmt(*struct.unpack("<HHIIHH", buffer[:16]))


def filter_chunk(
        function: Callable[[WavefileChunk], bool],
        wavchunk: WavefileChunk) -> Iterable[WavefileChunk]:

    if function(wavchunk):
        yield wavchunk
    for child in wavchunk.children:
        yield from filter_chunk(function, child)


def find_chunk(
        wavchunk: WavefileChunk,
        name: bytes=None,
        typename: bytes=None) -> Optional[WavefileChunk]:

    def comparator(wavchunk: WavefileChunk) -> bool:
        if name is not None:
            return wavchunk.name == name
        if typename is not None:
            return wavchunk.typename == typename

    try:
        return next(filter_chunk(comparator, wavchunk))
    except StopIteration:
        return None


def parse_info_chunk(infochunk: WavefileChunk) -> Dict[str, Union[str, bytes]]:
    return {bytes2str(child.name): bytes2str(child.data)
        for child in infochunk.children}

