from struct import unpack
from typing import BinaryIO
from uuid import UUID

from parser.datatypes.filenodechunkreference import FileChunkReference64x32, FileChunkReference32
from tools.repr import get_repr


class Header:
    ONE_GUID = UUID('{7B5C52E4-D88C-4DA7-AEB1-5378D02996D3}')
    ONETOC2_GUID = UUID('{43FF2FA1-EFD9-4C76-9EE2-10EA5722765F}')
    FILE_FORMAT_GUID = UUID('{109ADD3F-911B-49F5-A5D0-1791EDC8AED8}')
    HEADER_FORMAT = "<16s16s16s16sIIII8s8sIIQ8sIBBBB16sI12s12s12s12sQQ16sQ16sI12s12sIIII728s"

    guidFileType: UUID = None  # 16s
    guidFile: UUID = None  # 16s
    guidLegacyFileVersion: UUID = None  # 16s
    guidFileFormat: UUID = None  # 16s
    ffvLastCodeThatWroteToThisFile: int = None  # I
    ffvOldestCodeThatHasWrittenToThisFile: int = None  # I
    ffvNewestCodeThatHasWrittenToThisFile: int = None  # I
    ffvOldestCodeThatMayReadThisFile: int = None  # I
    fcrLegacyFreeChunkList: FileChunkReference32 = None  # 8s
    fcrLegacyTransactionLog: FileChunkReference32 = None  # 8s
    cTransactionsInLog: int = None  # I
    cbLegacyExpectedFileLength: int = None  # I
    rgbPlaceholder: int = None  # Q
    fcrLegacyFileNodeListRoot: FileChunkReference32 = None  # 8s
    cbLegacyFreeSpaceInFreeChunkList: int = None  # I
    fNeedsDefrag: int = None  # B                            # TODO maybe bool?
    fRepairedFile: int = None  # B                           # TODO "
    fNeedsGarbageCollect: int = None  # B                    # TODO "
    fHasNoEmbeddedFileObjects: int = None  # B               # TODO "
    guidAncestor: UUID = None  # 16s
    crcName: int = None  # I
    fcrHashedChunkList: FileChunkReference64x32 = None  # 12s
    fcrTransactionLog: FileChunkReference64x32 = None  # 12s
    fcrFileNodeListRoot: FileChunkReference64x32 = None  # 12s
    fcrFreeChunkList: FileChunkReference64x32 = None  # 12s
    cbExpectedFileLength: int = None  # Q
    cbFreeSpaceInFreeChunkList: int = None  # Q
    guidFileVersion: UUID = None  # 16s
    nFileVersionGeneration: int = None  # Q
    guidDenyReadFileVersion: UUID = None  # 16s
    grfDebugLogFlags: int = None  # I
    fcrDebugLog: FileChunkReference64x32 = None  # 12s
    fcrAllocVerificationFreeChunkList: FileChunkReference64x32 = None  # 12s
    bnCreated: int = None  # I
    bnLastWroteToThisFile: int = None  # I
    bnOldestWritten: int = None  # I
    bnNewestWritten: int = None  # I
    rgbReserved: bytes = None  # 728s

    def __init__(self, guidFileType: UUID, guidFile: UUID, guidLegacyFileVersion: UUID, guidFileFormat: UUID,
                 ffvLastCodeThatWroteToThisFile: int, ffvOldestCodeThatHasWrittenToThisFile: int,
                 ffvNewestCodeThatHasWrittenToThisFile: int, ffvOldestCodeThatMayReadThisFile: int,
                 fcrLegacyFreeChunkList: FileChunkReference32,
                 fcrLegacyTransactionLog: FileChunkReference32, cTransactionsInLog: int,
                 cbLegacyExpectedFileLength: int, rgbPlaceholder: int,
                 fcrLegacyFileNodeListRoot: FileChunkReference32, cbLegacyFreeSpaceInFreeChunkList: int,
                 fNeedsDefrag: int, fRepairedFile: int,
                 fNeedsGarbageCollect: int, fHasNoEmbeddedFileObjects: int, guidAncestor: UUID, crcName: int,
                 fcrHashedChunkList: FileChunkReference64x32,
                 fcrTransactionLog: FileChunkReference64x32, fcrFileNodeListRoot: FileChunkReference64x32,
                 fcrFreeChunkList: FileChunkReference64x32, cbExpectedFileLength: int,
                 cbFreeSpaceInFreeChunkList: int, guidFileVersion: UUID, nFileVersionGeneration: int,
                 guidDenyReadFileVersion: UUID,
                 grfDebugLogFlags: int, fcrDebugLog: FileChunkReference64x32,
                 fcrAllocVerificationFreeChunkList: FileChunkReference64x32, bnCreated: int, bnLastWroteToThisFile: int,
                 bnOldestWritten: int, bnNewestWritten: int, rgbReserved: bytes):
        self.guidFileType = guidFileType
        self.guidFile = guidFile
        self.guidLegacyFileVersion = guidLegacyFileVersion
        self.guidFileFormat = guidFileFormat
        self.ffvLastCodeThatWroteToThisFile = ffvLastCodeThatWroteToThisFile
        self.ffvOldestCodeThatHasWrittenToThisFile = ffvOldestCodeThatHasWrittenToThisFile
        self.ffvNewestCodeThatHasWrittenToThisFile = ffvNewestCodeThatHasWrittenToThisFile
        self.ffvOldestCodeThatMayReadThisFile = ffvOldestCodeThatMayReadThisFile
        self.fcrLegacyFreeChunkList = fcrLegacyFreeChunkList
        self.fcrLegacyTransactionLog = fcrLegacyTransactionLog
        self.cTransactionsInLog = cTransactionsInLog
        self.cbLegacyExpectedFileLength = cbLegacyExpectedFileLength
        self.rgbPlaceholder = rgbPlaceholder
        self.fcrLegacyFileNodeListRoot = fcrLegacyFileNodeListRoot
        self.cbLegacyFreeSpaceInFreeChunkList = cbLegacyFreeSpaceInFreeChunkList
        self.fNeedsDefrag = fNeedsDefrag
        self.fRepairedFile = fRepairedFile
        self.fNeedsGarbageCollect = fNeedsGarbageCollect
        self.fHasNoEmbeddedFileObjects = fHasNoEmbeddedFileObjects
        self.guidAncestor = guidAncestor
        self.crcName = crcName
        self.fcrHashedChunkList = fcrHashedChunkList
        self.fcrTransactionLog = fcrTransactionLog
        self.fcrFileNodeListRoot = fcrFileNodeListRoot
        self.fcrFreeChunkList = fcrFreeChunkList
        self.cbExpectedFileLength = cbExpectedFileLength
        self.cbFreeSpaceInFreeChunkList = cbFreeSpaceInFreeChunkList
        self.guidFileVersion = guidFileVersion
        self.nFileVersionGeneration = nFileVersionGeneration
        self.guidDenyReadFileVersion = guidDenyReadFileVersion
        self.grfDebugLogFlags = grfDebugLogFlags
        self.fcrDebugLog = fcrDebugLog
        self.fcrAllocVerificationFreeChunkList = fcrAllocVerificationFreeChunkList
        self.bnCreated = bnCreated
        self.bnLastWroteToThisFile = bnLastWroteToThisFile
        self.bnOldestWritten = bnOldestWritten
        self.bnNewestWritten = bnNewestWritten
        self.rgbReserved = rgbReserved

    @staticmethod
    def from_file(file: BinaryIO) -> 'Header':
        obj: Header = Header.__new__(Header)

        guidFileType, \
            guidFile, \
            guidLegacyFileVersion, \
            guidFileFormat, \
            ffvLastCodeThatWroteToThisFile, \
            ffvOldestCodeThatHasWrittenToThisFile, \
            ffvNewestCodeThatHasWrittenToThisFile, \
            ffvOldestCodeThatMayReadThisFile, \
            fcrLegacyFreeChunkList, \
            fcrLegacyTransactionLog, \
            cTransactionsInLog, \
            cbLegacyExpectedFileLength, \
            rgbPlaceholder, \
            fcrLegacyFileNodeListRoot, \
            cbLegacyFreeSpaceInFreeChunkList, \
            fNeedsDefrag, \
            fRepairedFile, \
            fNeedsGarbageCollect, \
            fHasNoEmbeddedFileObjects, \
            guidAncestor, \
            crcName, \
            fcrHashedChunkList, \
            fcrTransactionLog, \
            fcrFileNodeListRoot, \
            fcrFreeChunkList, \
            cbExpectedFileLength, \
            cbFreeSpaceInFreeChunkList, \
            guidFileVersion, \
            nFileVersionGeneration, \
            guidDenyReadFileVersion, \
            grfDebugLogFlags, \
            fcrDebugLog, \
            fcrAllocVerificationFreeChunkList, \
            bnCreated, \
            bnLastWroteToThisFile, \
            bnOldestWritten, \
            bnNewestWritten, \
            rgbReserved, = unpack(Header.HEADER_FORMAT, file.read(1024))

        guidFileType = UUID(bytes_le=guidFileType)
        guidFile = UUID(bytes_le=guidFile)
        guidLegacyFileVersion = UUID(bytes_le=guidLegacyFileVersion)
        guidFileFormat = UUID(bytes_le=guidFileFormat)
        guidAncestor = UUID(bytes_le=guidAncestor)
        guidFileVersion = UUID(bytes_le=guidFileVersion)
        guidDenyReadFileVersion = UUID(bytes_le=guidDenyReadFileVersion)

        fcrHashedChunkList = FileChunkReference64x32.from_bytes(fcrHashedChunkList)
        fcrTransactionLog = FileChunkReference64x32.from_bytes(fcrTransactionLog)
        fcrFileNodeListRoot = FileChunkReference64x32.from_bytes(fcrFileNodeListRoot)
        fcrFreeChunkList = FileChunkReference64x32.from_bytes(fcrFreeChunkList)
        fcrDebugLog = FileChunkReference64x32.from_bytes(fcrDebugLog)
        fcrAllocVerificationFreeChunkList = FileChunkReference64x32.from_bytes(fcrAllocVerificationFreeChunkList)

        fcrLegacyFreeChunkList = FileChunkReference32.from_bytes(fcrLegacyFreeChunkList)
        fcrLegacyTransactionLog = FileChunkReference32.from_bytes(fcrLegacyTransactionLog)
        fcrLegacyFileNodeListRoot = FileChunkReference32.from_bytes(fcrLegacyFileNodeListRoot)

        obj.__init__(guidFileType, guidFile, guidLegacyFileVersion, guidFileFormat, ffvLastCodeThatWroteToThisFile,
                     ffvOldestCodeThatHasWrittenToThisFile, ffvNewestCodeThatHasWrittenToThisFile,
                     ffvOldestCodeThatMayReadThisFile, fcrLegacyFreeChunkList, fcrLegacyTransactionLog,
                     cTransactionsInLog, cbLegacyExpectedFileLength, rgbPlaceholder, fcrLegacyFileNodeListRoot,
                     cbLegacyFreeSpaceInFreeChunkList, fNeedsDefrag, fRepairedFile, fNeedsGarbageCollect,
                     fHasNoEmbeddedFileObjects, guidAncestor, crcName, fcrHashedChunkList, fcrTransactionLog,
                     fcrFileNodeListRoot, fcrFreeChunkList, cbExpectedFileLength, cbFreeSpaceInFreeChunkList,
                     guidFileVersion, nFileVersionGeneration, guidDenyReadFileVersion, grfDebugLogFlags, fcrDebugLog,
                     fcrAllocVerificationFreeChunkList, bnCreated, bnLastWroteToThisFile, bnOldestWritten,
                     bnNewestWritten, rgbReserved)

        return obj

    def __repr__(self):
        return get_repr(self)
