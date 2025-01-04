import type { Transaction } from "$lib/models/Transaction";
import { TransactionStatus } from "$lib/models/TransactionStatus";
import type { UserDetails } from "$lib/models/UserDetails";

export function getCounterparty(transaction: Transaction): UserDetails {
    if (transaction.amount > 0) {
        return transaction.accountFrom.user;
    }

    return transaction.accountTo.user;
}

export function wasTransactionReverted(transaction: Transaction): boolean {
    if (transaction.status === TransactionStatus.REVERTED) {
        return true;
    }

    return false;
}