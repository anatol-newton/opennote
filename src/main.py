from logging import getLogger, error
from os import SEEK_SET
from typing import BinaryIO

from parser.basefile import BaseFile

log = getLogger()


def is_valid_onestore_file(file: BinaryIO) -> bool:
    file_type = file.read(16)

    file_types = [
        b"\xE4\x52\x5C\x7B\x8C\xD8\xA7\x4D\xAE\xB1\x53\x78\xD0\x29\x96\xD3",
        b"\xA1\x2F\xFF\x43\xD9\xEF\x76\x4C\x9E\xE2\x10\xEA\x57\x22\x76\x5F"
    ]

    if file_type in file_types:
        return True

    return False


def process_onenote_file(file: BinaryIO):
    valid_file = is_valid_onestore_file(file)
    if not valid_file:
        error("please provide valid One file")
        exit()

    file.seek(SEEK_SET)

    file_out: BaseFile = BaseFile.from_file(file)  # TODO distinguish OneStore and One

    print(file_out)


def main() -> None:
    with open("/path/to/onenote.file", "rb") as file:
        process_onenote_file(file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
