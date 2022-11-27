import gzip
import os.path


def decode_gzip_bytes(bytes_obj: bytes) -> str:
    return gzip.decompress(bytes_obj).decode()


def read_file(path: str, not_exist_default="1") -> str:
    if os.path.isfile(path):
        file = open(path, "r")
        content = file.read()
        file.close()
        return content
    file = open(path, "w+")
    file.write(not_exist_default)
    file.close()
    return not_exist_default
