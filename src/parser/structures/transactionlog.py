from os import SEEK_SET
from typing import BinaryIO, List

from parser.datatypes.filenodechunkreference import FileChunkReference64x32, FileNodeChunkReference
from parser.datatypes.transactionentry import TransactionEntry
from tools.repr import get_repr


class TransactionLogFragment:
    sizeTable: List[TransactionEntry] = []
    nextFragment: FileChunkReference64x32 = None

    def __init__(self, sizeTable: List[TransactionEntry], nextFragment: FileChunkReference64x32):
        self.sizeTable = sizeTable
        self.nextFragment = nextFragment

    @staticmethod
    def from_file(file: BinaryIO, transaction_log_chunk: FileNodeChunkReference) -> 'TransactionLogFragment':
        sizeTable: List[TransactionEntry] = []
        nextFragment: FileChunkReference64x32 = None

        file.seek(transaction_log_chunk.stp, SEEK_SET)

        sizeTable.append(TransactionEntry.from_bytes(file.read(8)))
        while sizeTable[-1].scrID != 0x00000001:
            sizeTable.append(TransactionEntry.from_bytes(file.read(8)))

        nextFragment = FileChunkReference64x32.from_bytes(file.read(12))

        return TransactionLogFragment(sizeTable, nextFragment)

    def __repr__(self):
        return get_repr(self)


class TransactionLog:
    transaction_log: List[TransactionEntry] = []
    transaction_log_fragments: List[TransactionLogFragment] = []

    def __init__(self, transaction_log: List[TransactionEntry],
                 transaction_log_fragments: List[TransactionLogFragment]):
        self.transaction_log = transaction_log
        self.transaction_log_fragments = transaction_log_fragments

    def __repr__(self):
        return get_repr(self)

    @staticmethod
    def from_file(file: BinaryIO, transaction_log_chunk: FileChunkReference64x32, transactions_in_log: int) -> 'TransactionLog':
        transaction_log_fragments = []
        transaction_log: List[TransactionEntry] = []

        transaction_log_fragments: List[TransactionLogFragment]

        if not transaction_log_chunk.is_FcrNil():
            transaction_log_fragments.append(TransactionLogFragment.from_file(file, transaction_log_chunk))

            # get all transaction log fragments
            while not transaction_log_fragments[-1].nextFragment.is_FcrNil():
                transaction_log_fragments.append(
                    TransactionLogFragment.from_file(file, transaction_log_fragments[-1].nextFragment))

        # create a complete transaction log
        for fragment in transaction_log_fragments:
            transaction_log.extend(fragment.sizeTable)

        # ignore non-committed log entries
        transaction_log = transaction_log[0:transactions_in_log]

        return TransactionLog(transaction_log, transaction_log_fragments)
