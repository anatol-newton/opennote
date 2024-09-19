from tools.repr import get_repr


class HashedChunkList:
    def __init__(self):
        # TODO depends on FileNode
        pass

    @staticmethod
    def from_file() -> 'HashedChunkList':
        pass

    def __repr__(self):
        return get_repr(self)