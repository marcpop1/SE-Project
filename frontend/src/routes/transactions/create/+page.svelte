<script lang="ts">
    import type { Account } from "$lib/models/Account";
    import { Currency } from "$lib/models/Currency";
    import { EnumUtils } from "$lib/utils/enum-utils";
    import { CreateTransactionPage } from "$lib/view-models/create-transaction-page";
    import { onMount } from "svelte";

    let account: Account | null;

    let username: string;
    let amount: number;
    let currency: string;
    let errorMessage: string = "";
    let currencies: string[] = [];

    const createTransactionPage = new CreateTransactionPage();
    const enumUtils = new EnumUtils();

    onMount(async () => {
        currencies = enumUtils.enumToArray(Currency);

        account = await createTransactionPage.onPageMount();
    });

    async function createTransaction(event: any) {
        event.preventDefault();
        
        errorMessage = await createTransactionPage.createTransaction(username, amount, currency);
    }
</script>

<div class="flex flex-col items-center gap-4">
    <h2 class="text-5xl my-5">
        Balance: {account?.balance}
        {account?.currency}
    </h2>
    <label class="form-control w-full max-w-xs">
        <div class="label">
            <span class="label-text">Username</span>
        </div>
        <input
            bind:value={username}
            type="text"
            placeholder="Type here"
            class="input input-bordered w-full max-w-xs"
        />
    </label>

    <label class="form-control w-full max-w-xs">
        <div class="label">
            <span class="label-text">Amount</span>
        </div>
        <input
            bind:value={amount}
            type="text"
            placeholder="Type here"
            class="input input-bordered w-full max-w-xs"
        />
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
        <button class="btn btn-wide btn-primary" on:click={createTransaction}
            >Create Transaction</button
        >
    </div>
</div>
