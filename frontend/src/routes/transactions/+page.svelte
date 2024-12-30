<script lang="ts">
    import type { Transaction } from "$lib/models/Transaction";
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
</script>

<div class="overflow-x-auto">
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
                                <div class="font-bold">{transaction.accountTo?.user.username}</div>
                            </div>
                        </div>
                    </td>
                    <td>{transaction.amount}</td>
                    <td>{transaction.currency}</td>
                    <td>{transaction.createdAt}</td>
                    <th>
                        <button class="btn btn-ghost btn-xs">details</button>
                    </th>
                </tr>
            {/each}
        </tbody>
        <tfoot>
        </tfoot>
    </table>
</div>
