import { goto } from "$app/navigation";

export class CardsPage {
    async onPageMount() {
        const response = await fetch("http://localhost:8000/cards", {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            const cards = await response.json();
            console.log(cards);
            return cards;
        } else {
            console.log("ERROR");
        }
    }

    async removeCard(cardId: number): Promise<void> {
        const response = await fetch(`http://localhost:8000/cards/${cardId}`, {
            method: "DELETE",
            credentials: "include",
        });

        if (response.ok) {
            window.location.reload();
        }
        else {
            console.log("ERROR");
        }
        
        return;
    }

    redirectToCreateCard() {
        goto("/cards/create");
    }
}