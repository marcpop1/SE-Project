<script lang="ts">
	import "../app.css";
	import { userRole } from "$lib/stores/userStore";
	import { UserRole } from "$lib/models/UserRole";
	import { afterNavigate, goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Header from "$lib/components/Header.svelte";
	import AdminHeader from "$lib/components/AdminHeader.svelte";
    import GuestHeader from "$lib/components/GuestHeader.svelte";
    import { RouteGuard } from "$lib/view-models/route-guard";

	let { children } = $props();

	const routeGuard = new RouteGuard();

	afterNavigate(async () => {
		routeGuard.checkRouteAccess($page);
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
