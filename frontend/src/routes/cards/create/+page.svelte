<script lang="ts">
    import { goto } from "$app/navigation";
    import { CardType } from "$lib/models/CardType";
    import { Currency } from "$lib/models/Currency";
    import { enumToArray } from "$lib/utils/enumUtils";
    import { onMount } from "svelte";

    let type: string;
    let currency: string;
    let errorMessage: string = "";
    let cardTypes: string[] = [];
    let currencies: string[] = [];

    onMount(() => {
        cardTypes = enumToArray(CardType);
        currencies = enumToArray(Currency);
    });

    async function createCard(event: any) {
        event.preventDefault();
        errorMessage = "";

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
            const data = await response.json();
            await goto("/cards");
        } else {
            const data = await response.json();
            errorMessage = data.detail;
        }
    }
</script>

<div class="flex flex-col items-center gap-4">
    <label class="form-control w-full max-w-xs">
        <div class="label">
            <span class="label-text">Type</span>
        </div>
        <select
            class="select select-bordered w-full max-w-xs"
            bind:value={type}
        >
            <option value="" disabled selected>Select card type</option>
            {#each cardTypes as cardType}
                <option value={cardType}>{cardType}</option>
            {/each}
        </select>
    </label>

    <label class="form-control w-full max-w-xs">
        <div class="label">
            <span class="label-text">Currency</span>
        </div>
        <select
            class="select select-bordered w-full max-w-xs"
            bind:value={currency}
        >
            <option value="" disabled selected>Select currency</option>
            {#each currencies as currency}
                <option value={currency}>{currency}</option>
            {/each}
        </select>
    </label>

    <div class="text-center">
        {#if errorMessage}
            <span class="text-red-600">{errorMessage}</span>
        {/if}
    </div>
    <div class="text-center">
        <button class="btn btn-wide btn-primary" on:click={createCard}
            >Create Card</button
        >
    </div>
</div>
