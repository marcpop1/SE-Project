import { goto } from "$app/navigation";

export class HomePage {
    async onPageMount() {
        const response = await fetch("http://localhost:8000/account_overview/", {
            credentials: "include",
        });

        if (response.ok) {
            const accountOverview = await response.json();
            return accountOverview;
        } else {
            await goto("/auth/login");
        }
    }
}