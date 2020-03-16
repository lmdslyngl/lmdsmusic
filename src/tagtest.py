
import sys
from musictag.tagloader import MusicMetadata


def main():
    # metadata = MusicMetadata.read(r"D:\Music\mp3,wav,wma\ガリレオ_福山雅治\01 vs. ～知覚と快楽の螺旋～.mp3")
    # metadata = MusicMetadata.read(r"D:\Music\mp3,wav,wma\CLICK.flac")
    # metadata = MusicMetadata.read(r"D:\Music\mp3,wav,wma\Mr.Children\Mr.Children 2003-2015 Thanksgiving 25\01 掌.m4a")
    # metadata = MusicMetadata.read(r"D:\Music\OriginalMusic\BeginningVillage_loop.flac")
    # metadata = MusicMetadata.read(r"D:\Music\OriginalMusic\BeginningVillage_loop.mp3")
    # print(metadata)

    music_files = [
        r"D:\Music\mp3,wav,wma\ガリレオ_福山雅治\01 vs. ～知覚と快楽の螺旋～.mp3",
        r"D:\Music\mp3,wav,wma\CLICK.flac",
        r"D:\Music\mp3,wav,wma\Mr.Children\Mr.Children 2003-2015 Thanksgiving 25\01 掌.m4a",
        r"D:\Music\OriginalMusic\BeginningVillage_loop.flac",
        r"D:\Music\OriginalMusic\BeginningVillage_loop.mp3",
        r"D:\Music\OriginalMusic\BattleTheme7.wav",
        r"D:\Music\OriginalMusic\BattleTheme7_loop.wav"
    ]
    for music_file in music_files:
        print(MusicMetadata.read(music_file))

    return 0


if __name__ == "__main__":
    sys.exit(main())
