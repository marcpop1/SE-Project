<script lang="ts">
    import { goto } from "$app/navigation";
    import type { Transaction } from "$lib/models/Transaction";
    import { getTransactionStatusString } from "$lib/models/TransactionStatus";
    import { onMount } from "svelte";

    let transactions: Transaction[];

    onMount(async () => {
        const response = await fetch("http://localhost:8000/transactions", {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            transactions = await response.json();
            console.log(transactions);
        }
    });

    function redirectToCreateTransaction() {
        goto("/transactions/create");
    }
</script>

<div class="h-max">
    <div class="overflow-x-auto transaction-list">
        <table class="table">
            <!-- head -->
            <thead>
                <tr>
                    <th>
                        <label>
                            <input type="checkbox" class="checkbox" />
                        </label>
                    </th>
                    <th>Name</th>
                    <th>Amount</th>
                    <th>Currency</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {#each transactions as transaction}
                    <tr>
                        <th>
                            <label>
                                <input type="checkbox" class="checkbox" />
                            </label>
                        </th>
                        <td>
                            <div class="flex items-center gap-3">
                                <div>
                                    <div class="font-bold">
                                        {transaction.accountTo?.user.name}
                                    </div>
                                </div>
                            </div>
                        </td>
                        <td>{transaction.amount}</td>
                        <td>{transaction.currency}</td>
                        <td>{transaction.type}</td>
                        <td>{getTransactionStatusString(transaction.status)}</td>
                        <td>{transaction.createdAt}</td>
                    </tr>
                {/each}
            </tbody>
            <tfoot> </tfoot>
        </table>
    </div>
    <div>
        <div class="text-center mt-16">
            <button
                class="btn btn-wide btn-primary"
                on:click={redirectToCreateTransaction}
                >Create New Transaction</button
            >
        </div>
    </div>
</div>

<style>
    .transaction-list {
        height: 40rem;
    }
</style>