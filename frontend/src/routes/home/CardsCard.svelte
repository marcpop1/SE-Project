<script lang="ts">
    import type { Card } from "$lib/models/Card";

    export let cards: Card[] = [];
</script>

<div
    class="w-full max-w-sm p-4 bg-white border border-gray-200 rounded-3xl shadow sm:p-6 dark:bg-gray-800 dark:border-gray-700"
>
    <div class="flex items-center justify-between mb-4">
        <h5
            class="mb-3 text-base font-semibold text-gray-900 md:text-xl dark:text-white"
        >
            Cards
        </h5>
        <a
            href="/"
            class="text-sm font-medium text-blue-600 hover:underline dark:text-blue-500"
        >
            View all
        </a>
    </div>
    <ul class="my-4 space-y-3">
        {#each cards as card}
            <li>
                <a
                    href="/"
                    class="flex items-center p-3 text-base font-bold text-gray-900 rounded-lg bg-gray-50 hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white"
                >
                    <span class="flex-1 ms-3 whitespace-nowrap"
                        >{card.type}</span
                    >
                    <span class="flex-2 ms-3 whitespace-nowrap"
                        >{card.currency}</span
                    >
                </a>
            </li>
        {/each}
    </ul>
</div>
