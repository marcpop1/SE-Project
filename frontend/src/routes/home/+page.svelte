<script lang="ts">
    import { onMount } from "svelte";
    import type { AccountOverview } from "$lib/models/AccountOverview";
    import BalanceCard from "$lib/components/BalanceCard.svelte";
    import CardsCard from "$lib/components/CardsCard.svelte";
    import TransactionsCard from "$lib/components/TransactionsCard.svelte";
    import { HomePage } from "$lib/view-models/home-page";

    let accountOverview: AccountOverview;
    const homePage = new HomePage();

    onMount(async () => {
        accountOverview = await homePage.onPageMount();
    });
</script>

<div class="home">
    <h1>Hello {accountOverview?.user.name}</h1>

    <div class="grid grid-cols-2 gap-16">
        <div>
            <BalanceCard
                balance={accountOverview?.account.balance}
                currency={accountOverview?.account.currency}
            />
            <br>
            <CardsCard cards={accountOverview?.cards} />
        </div>
        <div>
            <TransactionsCard transactions={accountOverview?.transactions} />
        </div>
    </div>
</div>

<style>
    .home {
        align-items: center;
        flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
    }
</style>