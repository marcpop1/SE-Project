import { goto } from "$app/navigation";
import type { Account } from "$lib/models/Account";

export class CreateTransactionPage {
    async onPageMount(): Promise<Account | null> {
        const response = await fetch("http://localhost:8000/accounts/user/", {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            const account = await response.json();
            console.log(account);
            return account;
        }

        return null;
    }

    async createTransaction(username: string, amount: number, currency: string): Promise<string> {
        const response = await fetch("http://localhost:8000/transactions/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                account_to_username: username,
                amount: amount,
                currency: currency,
            }),
        });

        if (response.ok) {
            await goto("/transactions");
            return "";
        } else {
            const data = await response.json();
            return data.detail;
        }
    }
}