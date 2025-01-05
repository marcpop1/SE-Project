<script lang="ts">
	import "../app.css";
	import { userRole } from "$lib/stores/userStore";
	import { UserRole } from "$lib/models/UserRole";
	import { afterNavigate, goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Header from "$lib/components/Header.svelte";
	import AdminHeader from "$lib/components/AdminHeader.svelte";
    import GuestHeader from "$lib/components/GuestHeader.svelte";

	let { children } = $props();

	afterNavigate(async () => {
		const role = localStorage.getItem("role");
		console.log("after navigate " + role);
		if (role) {
			userRole.set(role);
		} else {
			userRole.set(null);
		}

		if ($page.url.pathname === "/") {
			await goto("/auth/login");
			return;
		}
		else if ($page.url.pathname.startsWith("/auth") && role) {
			if (role === UserRole.ADMIN) {
				await goto("/admin");
				return;
			}

			await goto("/home");
			return;
		}
		else if (!$page.url.pathname.startsWith("/admin") && role === UserRole.ADMIN) {
			await goto("/admin");
			return;
		}
		else if ($page.url.pathname.startsWith("/admin") && role !== UserRole.ADMIN) {
			await goto("/home");
			return;
		}
	});
</script>

<div class="app">
	{#if $userRole === UserRole.USER}
		<Header />
	{:else if $userRole === UserRole.ADMIN}
		<AdminHeader />
	{:else}
		<GuestHeader />
	{/if}

	<main>
		{@render children()}
	</main>

	<footer>
		<p>SE Project</p>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 75rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
