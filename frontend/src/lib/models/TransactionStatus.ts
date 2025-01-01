export enum TransactionStatus {
    INITIATED = 0,
    IN_PROGRESS = 1,
    COMPLETED = 2,
    REVERTED = 3
}

export function getTransactionStatusString(status: number): string {
    return TransactionStatus[status].toLowerCase();
}