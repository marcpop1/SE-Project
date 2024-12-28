<script lang="ts">
    export let cards = [
        { currency: "RON" },
        { currency: "EUR" },
        { currency: "USD" },
        { currency: "GBP" },
        { currency: "RON" },
    ];
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
                        >{card.currency}</span
                    >
                    <span
                        class="inline-flex items-center justify-center px-2 py-0.5 ms-3 text-xs font-medium text-gray-500 bg-gray-200 rounded dark:bg-gray-700 dark:text-gray-400"
                    >
                        Popular
                    </span>
                </a>
            </li>
        {/each}
    </ul>
</div>
