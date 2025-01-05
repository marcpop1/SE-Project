<script lang="ts">
    import type { Transaction } from "$lib/models/Transaction";
    import { getTransactionStatusString } from "$lib/models/TransactionStatus";
    import { getCounterparty, wasTransactionReverted } from "$lib/utils/transactionUtils";
    import { TransactionsPage } from "$lib/view-models/transactions-page";
    import { onMount } from "svelte";

    let transactions: Transaction[];

    const transactionsPage = new TransactionsPage();

    onMount(async () => {
        transactions = await transactionsPage.onPageMount();
    });
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
                on:click={transactionsPage.redirectToCreateTransaction}
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