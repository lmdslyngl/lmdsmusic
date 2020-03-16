
from pathlib import Path

# スクリプトのあるディレクトリ
MY_DIR = Path(__file__).resolve().parent

# データディレクトリ
DATA_DIR = MY_DIR.parent / Path("data")

# 元データディレクトリ
SOURCE_DIR = DATA_DIR / Path("sources")

# 生成されたサイトのディレクトリ
GENERATED_SITE_DIR = DATA_DIR / Path("site_generated")

# サイトのテンプレートのディレクトリ
SITE_TEMPLATE_DIR = DATA_DIR / Path("site_template")

# 出力ストリームディレクトリ
STREAM_DIR = GENERATED_SITE_DIR / Path("stream")

# ffmpegへのパス
FFMPEG_PATH = MY_DIR / Path("ffmpeg.exe")
