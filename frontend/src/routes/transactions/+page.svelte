<script lang="ts">
    import { goto } from "$app/navigation";
    import type { Transaction } from "$lib/models/Transaction";
    import { getTransactionStatusString } from "$lib/models/TransactionStatus";
    import { getCounterparty, wasTransactionReverted } from "$lib/utils/transactionUtils";
    import { onMount } from "svelte";

    let transactions: Transaction[];

    onMount(async () => {
        const response = await fetch("http://localhost:8000/transactions", {
            method: "GET",
            credentials: "include",
        });

        if (response.ok) {
            const data = await response.json();
            transactions = data.map((transaction: any) => {
                const createdAt = new Date(transaction.createdAt);
                console.log('createdAt:', createdAt, 'isDate:', createdAt instanceof Date);
                return {
                    ...transaction,
                    createdAt
                };
            });
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
                    <th>Name</th>
                    <th>Amount</th>
                    <th>Currency</th>
                    <th>Converted Amount</th>
                    <th>Rate</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                {#each transactions as transaction}
                    <tr class={transaction.amount < 0 ? 'bg-red-100' : 'bg-green-100'}>
                        <td>
                            <div class="flex items-center gap-3">
                                <div>
                                    <div class="font-bold">
                                        {getCounterparty(transaction).name}
                                    </div>
                                </div>
                            </div>
                        </td>
                        <td>{transaction.amount}</td>
                        <td>{transaction.currency}</td>
                        <td>{transaction.convertedAmount}</td>
                        <td>{transaction.rate}</td>
                        <td>{transaction.type}</td>
                        <td class={wasTransactionReverted(transaction) ? 'bg-red-300' : ''}>{getTransactionStatusString(transaction.status)}</td>
                        <td>{transaction.createdAt?.toLocaleString()}</td>
                    </tr>
                {/each}
            </tbody>
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