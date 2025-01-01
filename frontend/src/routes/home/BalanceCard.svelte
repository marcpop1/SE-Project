<script lang="ts">
    import { goto, invalidate } from "$app/navigation";

    export let balance: number = 0;
    export let currency: string = "RON";

    let addAmount: number;

    let showModal = false;

    function openModal() {
        showModal = true;
    }

    function closeModal() {
        showModal = false;
    }

    async function addMoney(event: any) {
        event.preventDefault();

        const response = await fetch("http://localhost:8000/transactions/add-money/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: 'include',
            body: JSON.stringify({
                amount: addAmount
            }),
        });

        if (response.ok) {
            console.log(await response.json());
            window.location.reload();
        }
    }
</script>

<div class="card bg-primary text-primary-content w-96 rounded-3xl">
    <div class="card-body">
        <h2 class="card-title">Balance:</h2>
        <p class="text-5xl">{balance} {currency}</p>
        <div class="card-actions justify-end">
            <button class="btn" on:click={openModal}>Add money</button>
        </div>
    </div>
</div>

<!-- Modal -->
{#if showModal}
    <div
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
        <div class="bg-white rounded-lg shadow-lg w-96 p-6">
            <!-- Modal Header -->
            <h3 class="text-lg font-bold mb-4">Add Money</h3>

            <!-- Modal Content -->
            <form on:submit={addMoney}>
                <div class="form-control">
                    <label class="label" for="money">
                        <span class="label-text">Amount</span>
                    </label>
                    <input bind:value={addAmount}
                        name="money"
                        type="number"
                        min="0"
                        step="0.01"
                        class="input input-bordered w-full"
                        placeholder="Enter amount"
                        required
                    />
                </div>

                <!-- Modal Actions -->
                <div class="mt-4 flex justify-end gap-2">
                    <button
                        type="button"
                        class="btn btn-outline"
                        on:click={closeModal}>Cancel</button
                    >
                    <button type="submit" class="btn btn-primary">Add</button>
                </div>
            </form>
        </div>
    </div>
{/if}
