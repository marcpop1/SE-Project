<script lang="ts">
    import { onMount } from "svelte";
    import BalanceCard from "./BalanceCard.svelte";
    import CardsCard from "./CardsCard.svelte";
    import TransactionsCard from "./TransactionsCard.svelte";
    import { goto } from "$app/navigation";

    let currentUser = { balance: 2, currency: "EUR", cards: [] };
    let user = { User: { username: null } };

    onMount(async () => {
        const response = await fetch("http://localhost:8000/", {
            credentials: "include",
        });

        if (response.ok) {
            user = await response.json();
            console.log(user);
        } else {
            await goto("/auth/login");
        }
    });

    async function logout() {
        try {
            const response = await fetch("http://localhost:8000/auth/logout", {
                method: "POST",
                credentials: "include"
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
    <h1>Hello {user.User.username}</h1>
    <button on:click={logout}>Logout</button>

    <div class="grid grid-cols-2 gap-4">
        <div>
            <BalanceCard
                balance={currentUser.balance}
                currency={currentUser.currency}
            />
            <br />
            <CardsCard />
        </div>
        <div>
            <TransactionsCard />
        </div>
    </div>
</div>
