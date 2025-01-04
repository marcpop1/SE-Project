<script lang="ts">
    import { goto } from "$app/navigation";
    import type { Card } from "$lib/models/Card";
    import { onMount } from "svelte";

    let cards: Card[] = [];

    onMount(async () => {
        const response = await fetch("http://localhost:8000/cards", {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            cards = await response.json();
            console.log(cards);
        } else {
            console.log("ERROR");
        }
    });

    function redirectToCreateCard() {
        goto("/cards/create");
    }

    async function removeCard(cardId: number): Promise<void> {
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
</script>

<div class="h-max">
    <div class="overflow-x-auto card-list">
        <table class="table">
            <!-- head -->
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Currency</th>
                    <th>Number</th>
                    <th>Expiration Month</th>
                    <th>Expiration Year</th>
                    <th>CVV</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {#if cards?.length > 0}
                    {#each cards as card}
                        <tr>
                            <td>{card.type}</td>
                            <td>{card.currency}</td>
                            <td>{card.number}</td>
                            <td>{card.expirationMonth}</td>
                            <td>{card.expirationYear}</td>
                            <td>{card.cvv}</td>
                            <th>
                                <button
                                    class="btn btn-ghost btn-xs"
                                    on:click={async () =>
                                        await removeCard(card.id)}
                                    >Remove</button
                                >
                            </th>
                        </tr>
                    {/each}
                {:else}
                    <tr>
                        <td colspan="4">No cards available</td>
                    </tr>
                {/if}
            </tbody>
            <tfoot> </tfoot>
        </table>
    </div>
    <div>
        <div class="text-center mt-16">
            <button
                class="btn btn-wide btn-primary"
                on:click={redirectToCreateCard}>Create New Card</button
            >
        </div>
    </div>
</div>

<style>
    .card-list {
        height: 40rem;
    }
</style>
