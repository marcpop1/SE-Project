<script lang="ts">
    import type { Transaction } from "$lib/models/Transaction";
    import { TransactionType } from "$lib/models/TransactionType";
    import { TransactionUtils } from "$lib/utils/transaction-utils";

    export let transactions: Transaction[] = [];

    const transactionUtils = new TransactionUtils();

    function isTopUpTransaction(transaction: Transaction): boolean {
        if (transaction.type === TransactionType.TOP_UP) {
            return true;
        }

        return false;
    }

    function getTransactionDisplayName(transaction: Transaction): string {
        if (isTopUpTransaction(transaction)) {
            return transaction.type;
        }

        return transactionUtils.getCounterparty(transaction).name;
    }
</script>

<div
    class="w-full max-w-md p-4 bg-white border border-gray-200 rounded-3xl shadow sm:p-8 dark:bg-gray-800 dark:border-gray-700"
>
    <div class="flex items-center justify-between mb-4">
        <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white">
            Transactions
        </h5>
        <a href="/transactions" class="text-sm font-medium text-blue-600 hover:underline dark:text-blue-500">
            View all
        </a>
    </div>
    <div class="flow-root">
        <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
            {#each transactions as transaction}
                <li class="py-3 sm:py-4">
                    <div class="flex items-center">
                        <div class="flex-1 min-w-0 ms-4">
                            <p class="text-sm font-medium text-gray-900 truncate dark:text-white">
                                {getTransactionDisplayName(transaction)}
                            </p>
                        </div>
                        <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                            {transaction.amount} {transaction.currency}
                        </div>
                    </div>
                </li>
            {/each}
        </ul>
    </div>
</div>
