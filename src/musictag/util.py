
class TagLoaderException(Exception):
    pass


def str2int(s: str, default=0) -> int:
    try:
        return int(s)
    except ValueError:
        return default


def get_or_default(d, k, default=""):
    if k in d:
        return d[k]
    else:
        return default


def bytes2str(buffer: bytes) -> [str, bytes]:
    # 末尾のNULL文字を削除する
    while buffer[-1] == 0:
        buffer = buffer[:-1]

    for encoding in ["Shift-JIS", "UTF-8"]:
        try:
            return buffer.decode(encoding)
        except UnicodeDecodeError:
            pass
    return buffer
