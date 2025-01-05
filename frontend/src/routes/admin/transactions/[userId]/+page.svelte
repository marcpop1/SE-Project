<script lang="ts">
    import { page } from "$app/stores";
    import type { Account } from "$lib/models/Account";
    import type { Transaction } from "$lib/models/Transaction";
    import { getTransactionStatusString } from "$lib/models/TransactionStatus";
    import { getCounterparty, wasTransactionReverted } from "$lib/utils/transactionUtils";
    import { AdminViewUserTransactionsPage } from "$lib/view-models/admin-view-user-transactions-page";
    import { onMount } from "svelte";

    let userId: string;
    let transactions: Transaction[] = [];
    let account: Account | null = null;

    $: userId = $page.params.userId;

    const adminViewUserTransactionsPage = new AdminViewUserTransactionsPage();

    onMount(async () => {
        account = await adminViewUserTransactionsPage.getAccount(userId);
        transactions = await adminViewUserTransactionsPage.getTransactions(userId);
    });
</script>

<div class="h-max">
    <h1>{account?.user.name}</h1>
    <h1>Balance: {account?.balance} {account?.currency}</h1>
    <div class="overflow-x-auto transaction-list">
        <table class="table">
            <!-- head -->
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Account holder username</th>
                    <th>Account holder name</th>
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
                    <tr
                        class={transaction.amount < 0
                            ? "bg-red-100"
                            : "bg-green-100"}
                    >
                        <td>{transaction.id}</td>
                        <td>{getCounterparty(transaction).username}</td>
                        <td>{getCounterparty(transaction).name}</td>
                        <td>{transaction.amount}</td>
                        <td>{transaction.currency}</td>
                        <td>{transaction.convertedAmount}</td>
                        <td>{transaction.rate}</td>
                        <td>{transaction.type}</td>
                        <td class={wasTransactionReverted(transaction) ? 'bg-red-300' : ''}>{getTransactionStatusString(transaction.status)}</td
                        >
                        <td>{transaction.createdAt?.toLocaleString()}</td>
                        <th>
                            {#if adminViewUserTransactionsPage.canReverseTransaction(transaction)}
                                <button
                                    class="btn btn-ghost btn-xs"
                                    on:click={async () =>
                                        await adminViewUserTransactionsPage.reverseTransaction(
                                            transaction.id,
                                        )}>Reverse transaction</button
                                >
                            {/if}
                        </th>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>

<style>
    .transaction-list {
        height: 35rem;
    }
</style>
