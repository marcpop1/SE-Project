from enum import Enum

class TransactionStatus(int, Enum):
    INITIATED = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    REVERTED = 3