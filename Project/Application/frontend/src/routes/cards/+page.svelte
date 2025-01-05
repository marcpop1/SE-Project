<script lang="ts">
    import { goto } from "$app/navigation";
    import type { Card } from "$lib/models/Card";
    import { CardsPage } from "$lib/view-models/cards-page";
    import { onMount } from "svelte";

    let cards: Card[] = [];

    const cardsPage = new CardsPage();

    onMount(async () => {
        cards = await cardsPage.onPageMount();
    });
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
                                        await cardsPage.removeCard(card.id)}
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
                on:click={cardsPage.redirectToCreateCard}>Create New Card</button
            >
        </div>
    </div>
</div>

<style>
    .card-list {
        height: 40rem;
    }
</style>
