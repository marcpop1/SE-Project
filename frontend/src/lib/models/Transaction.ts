import type { Account } from "./Account";
import type { TransactionStatus } from "./TransactionStatus";
import type { TransactionType } from "./TransactionType";

export interface Transaction {
    id: number;
    accountFromId: number;
    accountToId: number;
    amount: number;
    currency: string;
    convertedAmount: number;
    rate: number;
    status: TransactionStatus;
    type: TransactionType;
    createdAt: Date;
    accountFrom: Account;
    accountTo: Account;
}