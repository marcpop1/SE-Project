<script lang="ts">
    import { page } from "$app/stores";
    import type { Account } from "$lib/models/Account";
    import type { Transaction } from "$lib/models/Transaction";
    import {
        getTransactionStatusString,
        TransactionStatus,
    } from "$lib/models/TransactionStatus";
    import { TransactionType } from "$lib/models/TransactionType";
    import { getCounterparty, wasTransactionReverted } from "$lib/utils/transactionUtils";
    import { onMount } from "svelte";

    let userId: string;
    let transactions: Transaction[] = [];
    let account: Account | null = null;

    $: userId = $page.params.userId;

    onMount(async () => {
        account = await getAccount();
        transactions = await getTransactions();
    });

    async function getAccount(): Promise<Account | null> {
        const response = await fetch(
            `http://localhost:8000/admin/account/${userId}`,
            {
                method: "GET",
                credentials: "include",
            },
        );

        if (response.ok) {
            const account = await response.json();
            console.log(account);
            return account;
        }

        return null;
    }

    async function getTransactions(): Promise<Transaction[]> {
        const response = await fetch(
            `http://localhost:8000/admin/transactions/${userId}`,
            {
                method: "GET",
                credentials: "include",
            },
        );

        if (response.ok) {
            const data = await response.json();
            transactions = data.map((transaction: any) => {
                const createdAt = new Date(transaction.createdAt);
                console.log(
                    "createdAt:",
                    createdAt,
                    "isDate:",
                    createdAt instanceof Date,
                );
                return {
                    ...transaction,
                    createdAt,
                };
            });
            console.log(transactions);
            return transactions;
        }

        return [];
    }

    async function reverseTransaction(transactionId: number): Promise<void> {
        const response = await fetch(
            `http://localhost:8000/admin/transactions/${transactionId}/revert/`,
            {
                method: "PUT",
                credentials: "include",
            },
        );

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            window.location.reload();
        }
    }

    function canReverseTransaction(transaction: Transaction): boolean {
        return (
            transaction.type == TransactionType.TRANSFER &&
            transaction.status == TransactionStatus.COMPLETED
        );
    }
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
                            {#if canReverseTransaction(transaction)}
                                <button
                                    class="btn btn-ghost btn-xs"
                                    on:click={async () =>
                                        await reverseTransaction(
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
