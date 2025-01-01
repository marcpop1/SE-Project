<script lang="ts">
    import { onMount } from "svelte";
    import BalanceCard from "./BalanceCard.svelte";
    import CardsCard from "./CardsCard.svelte";
    import TransactionsCard from "./TransactionsCard.svelte";
    import { goto } from "$app/navigation";
    import type { AccountOverview } from "$lib/models/AccountOverview";

    let accountOverview: AccountOverview;

    onMount(async () => {
        const response = await fetch("http://localhost:8000/", {
            credentials: "include",
        });

        if (response.ok) {
            accountOverview = await response.json();
            console.log(accountOverview);
        } else {
            await goto("/auth/login");
        }
    });

    async function logout() {
        try {
            const response = await fetch("http://localhost:8000/auth/logout", {
                method: "POST",
                credentials: "include",
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Logout successful:", data);
            goto("/auth/login");
        } catch (error) {
            console.error("Failed to logout:", error);
        }
    }
</script>

<div class="home">
    <h1>Hello {accountOverview?.user.name}</h1>
    <button on:click={logout}>Logout</button>

    <div class="grid grid-cols-2 gap-4">
        <div>
            <BalanceCard
                balance={accountOverview?.account.balance}
                currency={accountOverview?.account.currency}
            />
            <br />
            <CardsCard cards={accountOverview?.cards} />
        </div>
        <div>
            <TransactionsCard transactions={accountOverview?.transactions} />
        </div>
    </div>
</div>