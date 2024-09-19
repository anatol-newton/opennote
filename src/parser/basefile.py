from typing import BinaryIO

from parser.structures.filenodelist import FileNodeList
from parser.structures.freechunklist import FreeChunkList
from parser.structures.hashedchunklist import HashedChunkList
from parser.structures.header import Header
from parser.structures.transactionlog import TransactionLog
from tools.repr import get_repr


class BaseFile(object):
    header: Header = None
    freechunklist: FreeChunkList = None
    transactionlog: TransactionLog = None
    hashedchunklist: HashedChunkList = None
    filenodelist: FileNodeList = None

    def __init__(self, header: Header, freechunklist: FreeChunkList, transactionlog: TransactionLog,
                 hashedchunklist: HashedChunkList, filenodelist: FileNodeList):
        self.header = header
        self.freechunklist = freechunklist
        self.transactionlog = transactionlog
        self.hashedchunklist = hashedchunklist
        self.filenodelist = filenodelist


    @staticmethod
    def from_file(file: BinaryIO) -> 'BaseFile':
        header = Header.from_file(file)
        freechunklist = FreeChunkList.from_file(file, header.fcrFreeChunkList)
        transactionlog = TransactionLog.from_file(file, header.fcrTransactionLog, header.cTransactionsInLog)
        hashedchunklist = HashedChunkList.from_file()
        filenodelist = FileNodeList.from_file()

        return BaseFile(header, freechunklist, transactionlog, hashedchunklist, filenodelist)

    def __repr__(self):
        return get_repr(self)
