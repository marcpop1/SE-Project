<script>
    import BalanceCard from "./BalanceCard.svelte";
    import CardsCard from "./CardsCard.svelte";
    import TransactionsCard from "./TransactionsCard.svelte";

    let currentUser = { balance: 2, currency: "EUR", cards: [] };
</script>

<div class="home">
    <h1>Dashboard</h1>

    <div class="grid grid-cols-2 gap-4">
        <div>
            <BalanceCard balance={currentUser.balance} currency={currentUser.currency} />
            <br>
            <CardsCard />
        </div>
        <div>
            <TransactionsCard />
        </div>
    </div>
</div>
