from struct import unpack


class TransactionEntry:
    TRANSACTION_ENTRY_FORMAT = "<II"

    scrID = None  # I
    transactionEntrySwitch = None  # I

    def __init__(self, scrID: int, transactionEntrySwitch: int):
        self.scrID = scrID
        self.transactionEntrySwitch = transactionEntrySwitch

    @staticmethod
    def from_bytes(data_bytes: bytes) -> 'TransactionEntry':
        scrID, transactionEntrySwitch = unpack(TransactionEntry.TRANSACTION_ENTRY_FORMAT, data_bytes)
        return TransactionEntry(scrID, transactionEntrySwitch)

    def __repr__(self):
        return f'TransactionEntry(scrID={self.scrID}, transactionEntrySwitch={self.transactionEntrySwitch})'