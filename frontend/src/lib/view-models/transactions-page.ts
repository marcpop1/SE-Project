import { goto } from "$app/navigation";
import type { Transaction } from "$lib/models/Transaction";

export class TransactionsPage {
    async onPageMount(): Promise<Transaction[]> {
        const response = await fetch("http://localhost:8000/transactions", {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            const data = await response.json();
            const transactions = data.map((transaction: any) => {
                const createdAt = new Date(transaction.createdAt);
                console.log('createdAt:', createdAt, 'isDate:', createdAt instanceof Date);
                return {
                    ...transaction,
                    createdAt
                };
            });
            console.log(transactions);
            return transactions;
        }

        return [];
    }

    redirectToCreateTransaction() {
        goto("/transactions/create");
    }
}