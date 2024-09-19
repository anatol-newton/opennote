from struct import unpack


class FileNodeChunkReference:
    stp: int = None
    cb: int = None
    invalid: int = None

    def __init__(self, stp, cb, invalid):
        self.stp = stp
        self.cb = cb
        self.invalid = invalid

    @staticmethod
    def from_bytes(data_bytes: bytes, stp_format: int, cb_format: int):
        data_size: int = 0
        stp_compressed: bool = False
        stp_type: str = ''
        invalid: int = 0x0
        if stp_format == 0:
            stp_type = 'Q'
            data_size += 8
            invalid = 0xffffffffffffffff
        elif stp_format == 1:
            stp_type = 'I'
            data_size += 4
            invalid = 0xffffffff
        elif stp_format == 2:
            stp_type = 'H'
            data_size += 2
            stp_compressed = True
            invalid = 0x7fff8
        elif stp_format == 3:
            stp_type = 'I'
            data_size += 4
            stp_compressed = True
            invalid = 0x7fffffff8

        cb_type: str = ''
        cb_compressed: bool = False
        if cb_format == 0:
            cb_type = 'I'
            data_size += 4
        elif cb_format == 1:
            cb_type = 'Q'
            data_size += 8
        elif cb_format == 2:
            cb_type = 'B'
            data_size += 1
            cb_compressed = True
        elif cb_format == 3:
            cb_type = 'H'
            data_size += 2
            cb_compressed = True

        stp: int = 0
        cb: int = 0
        stp, cb = unpack(f'<{stp_type}{cb_type}', data_bytes)
        if stp_compressed:
            stp *= 8

        if cb_compressed:
            cb *= 8

        return FileNodeChunkReference(stp, cb, invalid)

    def is_FcrNil(self):
        return (self.stp & self.invalid) == self.invalid and self.cb == 0

    def is_FcrZero(self):
        return self.stp == 0 and self.cb == 0

    def is_FcrNilZero(self):
        return self.is_FcrNil() or self.is_FcrZero()

    def __repr__(self):
        return f'{self.__class__.__name__}(stp={self.stp}, cb={self.cb})'


class FileChunkReference32(FileNodeChunkReference):
    def __init__(self, stp, cb):
        super().__init__(stp, cb, 0xffffffff)

    @staticmethod
    def from_bytes(data_bytes: bytes, *args, **kwargs) -> 'FileChunkReference32':
        filechunkreference: FileNodeChunkReference = super().from_bytes(data_bytes, 1, 0)
        return FileChunkReference32(filechunkreference.stp, filechunkreference.cb)


class FileChunkReference64x32(FileNodeChunkReference):
    def __init__(self, stp, cb):
        super().__init__(stp, cb, 0xffffffffffffffff)

    @staticmethod
    def from_bytes(data_bytes: bytes, *args, **kwargs) -> 'FileChunkReference64x32':
        filechunkreference: FileNodeChunkReference = super().from_bytes(data_bytes, 1, 0)
        return FileChunkReference64x32(filechunkreference.stp, filechunkreference.cb)


class FileChunkReference64(FileNodeChunkReference):
    def __init__(self, stp, cb):
        super().__init__(stp, cb, 0xffffffffffffffff)

    @staticmethod
    def from_bytes(data_bytes: bytes, *args, **kwargs) -> 'FileChunkReference64':
        filechunkreference: FileNodeChunkReference = super().from_bytes(data_bytes, 1, 0)
        return FileChunkReference64(filechunkreference.stp, filechunkreference.cb)
