import struct

from tools.repr import get_repr


class FileNodeListHeader:
    FILENODELISTHEADER_FORMAT = "<QII"

    uintMagic: int = None
    fileNodeListID: int = None
    nFragmentSequence: int = None

    def __init__(self, uintMagic: int, fileNodeListID: int, nFragmentSequence: int):
        self.uintMagic = uintMagic
        self.fileNodeListID = fileNodeListID
        self.nFragmentSequence = nFragmentSequence

    def __repr__(self):
        get_repr(self)

    @staticmethod
    def from_bytes(data_bytes: bytes) -> 'FileNodeListHeader':
        uintMagic: int = None  # Q
        fileNodeListID: int = None  # I
        nFragmentSequence: int = None  # I

        uintMagic, \
            fileNodeListID, \
            nFragmentSequence = struct.unpack(FileNodeListHeader.FILENODELISTHEADER_FORMAT, data_bytes)

        return FileNodeListHeader(uintMagic, fileNodeListID, nFragmentSequence)
