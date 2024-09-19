from os import SEEK_SET
from struct import unpack
from typing import BinaryIO, List

from parser.datatypes.filenodechunkreference import FileNodeChunkReference, FileChunkReference64x32, \
    FileChunkReference64
from tools.repr import get_repr


class FreeChunkListFragment:
    FREE_CHUNK_LIST_FRAGMENT_FORMAT = "<I12s"
    FREE_CHUNK_LIST_FCRFREECHUNK_FORMAT = "<16s"

    crc: int = None
    fcrNextChunk: FileChunkReference64x32 = None
    fcrFreeChunk: List[FileChunkReference64] = []

    def __init__(self, crc: int, fcrNextChunk: FileChunkReference64x32, fcrFreeChunk: List[FileChunkReference64]):
        self.crc = crc
        self.fcrNextChunk = fcrNextChunk
        self.fcrFreeChunk = fcrFreeChunk

    @staticmethod
    def from_file(file: BinaryIO, file_chunk_reference: FileNodeChunkReference) -> 'FreeChunkListFragment':
        crc = None  # I
        fcrNextChunk = None  # 12s
        fcrFreeChunk: List[FileChunkReference64] = []

        # go to start of FreeChunkList
        file.seek(file_chunk_reference.stp, SEEK_SET)

        # read crc and fcrNextChunk
        crc, \
            fcrNextChunk = unpack(FreeChunkListFragment.FREE_CHUNK_LIST_FRAGMENT_FORMAT, file.read(16))

        # convert to FileChunkReference
        fcrNextChunk = FileChunkReference64x32.from_bytes(fcrNextChunk)

        # read fcrFreeChunk (variable size, calculated by cb of fcrFreeChunkList)
        for i in range(0, int((file_chunk_reference.cb - 16) / 16)):
            fcrFreeChunk.append(FileChunkReference64.from_bytes(file.read(16)))

        return FreeChunkListFragment(crc, fcrNextChunk, fcrFreeChunk)

    def __repr__(self):
        return get_repr(self)


class FreeChunkList:
    free_chunk_fragments: List[FreeChunkListFragment] = []
    free_chunks: List[FileChunkReference64] = []

    def __init__(self, free_chunk_fragments: List[FreeChunkListFragment], free_chunks: List[FileChunkReference64]):
        self.free_chunk_fragments = free_chunk_fragments
        self.free_chunks = free_chunks

    @staticmethod
    def from_file(file: BinaryIO, free_chunk_list: FileChunkReference64x32) -> 'FreeChunkList':
        free_chunk_fragments: List[FreeChunkListFragment] = []
        free_chunks: List[FileChunkReference64] = []

        # check if FreeChunkList exists
        if not free_chunk_list.is_FcrNilZero():
            free_chunk_fragments.append(FreeChunkListFragment.from_file(file, free_chunk_list))

            # get all the FreeChunkListFragments
            while not free_chunk_fragments[-1].fcrNextChunk.is_FcrNilZero():
                free_chunk_fragments.append(
                    FreeChunkListFragment.from_file(file, free_chunk_fragments[-1].fcrNextChunk))

        # create a complete list of all free chunks
        for fragment in free_chunk_fragments:
            free_chunks.extend(fragment.fcrFreeChunk)

        return FreeChunkList(free_chunk_fragments, free_chunks)

    def __repr__(self):
        return get_repr(self)
