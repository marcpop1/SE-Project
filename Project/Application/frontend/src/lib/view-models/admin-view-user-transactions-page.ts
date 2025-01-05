import type { Account } from "$lib/models/Account";
import type { Transaction } from "$lib/models/Transaction";
import { TransactionStatus } from "$lib/models/TransactionStatus";
import { TransactionType } from "$lib/models/TransactionType";

export class AdminViewUserTransactionsPage {
    async getAccount(userId: string): Promise<Account | null> {
        const response = await fetch(
            `http://localhost:8000/admin/account/${userId}`,
            {
                method: "GET",
                credentials: "include",
            },
        );

        if (response.ok) {
            const account = await response.json();
            console.log(account);
            return account;
        }

        return null;
    }

    async getTransactions(userId: string): Promise<Transaction[]> {
        const response = await fetch(
            `http://localhost:8000/admin/transactions/${userId}`,
            {
                method: "GET",
                credentials: "include",
            },
        );

        if (response.ok) {
            const data = await response.json();
            const transactions = data.map((transaction: any) => {
                const createdAt = new Date(transaction.createdAt);
                console.log(
                    "createdAt:",
                    createdAt,
                    "isDate:",
                    createdAt instanceof Date,
                );
                return {
                    ...transaction,
                    createdAt,
                };
            });
            console.log(transactions);
            return transactions;
        }

        return [];
    }

    async reverseTransaction(transactionId: number): Promise<void> {
        const response = await fetch(
            `http://localhost:8000/admin/transactions/${transactionId}/revert/`,
            {
                method: "PUT",
                credentials: "include",
            },
        );

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            window.location.reload();
        }
    }

    canReverseTransaction(transaction: Transaction): boolean {
        return (
            transaction.type == TransactionType.TRANSFER &&
            transaction.status == TransactionStatus.COMPLETED
        );
    }
}