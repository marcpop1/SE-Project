import { goto } from "$app/navigation";
import type { UserDetails } from "$lib/models/UserDetails";

export class AdminHomePage {
    async onPageMount(): Promise<UserDetails[]> {
        const response = await fetch("http://localhost:8000/admin/users/", {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            const users = await response.json();
            console.log(users);
            return users;
        }

        return [];
    }

    redirectToUserTransactions(userId: number): undefined {
        goto(`admin/transactions/${userId}`);
    }
}