import { goto } from "$app/navigation";

export class CreateCardPage {
    async createCard(type: string, currency: string): Promise<string> {
        const response = await fetch("http://localhost:8000/cards/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({
                type: type,
                currency: currency,
            }),
        });

        if (response.ok) {
            await goto("/cards");
            return "";
        } else {
            const data = await response.json();
            return data.detail;
        }
    }
}