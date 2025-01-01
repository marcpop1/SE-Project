import type { Account } from "./Account";
import type { TransactionStatus } from "./TransactionStatus";

export interface Transaction {
    id: number;
    accountFromId: number;
    accountToId: number;
    amount: number;
    currency: string;
    status: TransactionStatus;
    type: string;
    createdAt: Date;
    accountFrom: Account;
    accountTo: Account;
}