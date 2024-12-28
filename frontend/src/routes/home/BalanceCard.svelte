<script lang='ts'>
    export let balance: number = 0;
    export let currency: string = 'RON';
</script>

<div class="card bg-primary text-primary-content w-96 rounded-3xl">
    <div class="card-body">
        <h2 class="card-title">Balance:</h2>
        <p class="text-5xl">{balance} {currency}</p>
        <div class="card-actions justify-end">
            <button class="btn">Add money</button>
        </div>
    </div>
</div>