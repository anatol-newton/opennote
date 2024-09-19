from tools.repr import get_repr


class FileNodeListFragment:
    def __init__(self):
        pass

    def __repr__(self):
        return get_repr(self)

    @staticmethod
    def from_file() -> 'FileNodeListFragment':
        pass


class FileNodeList:

    def __init__(self):
        pass

    def __repr__(self):
        return get_repr(self)

    @staticmethod
    def from_file() -> 'FileNodeList':
        pass
