<script lang="ts">
    import type { UserDetails } from "$lib/models/UserDetails";
    import { AdminHomePage } from "$lib/view-models/admin-home-page";
    import { onMount } from "svelte";

    let users: UserDetails[];

    const adminHomePage = new AdminHomePage();

    onMount(async () => {
        users = await adminHomePage.onPageMount();
    });
</script>

<div class="h-max">
    <div class="overflow-x-auto user-list">
        <table class="table">
            <!-- head -->
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Name</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {#each users as user}
                    <tr class="hover" on:click={adminHomePage.redirectToUserTransactions(user.id)}>
                        <td>
                            <div class="flex items-center gap-3">
                                <div>
                                    <div class="font-bold">
                                        {user.id}
                                    </div>
                                </div>
                            </div>
                        </td>
                        <td>{user.username}</td>
                        <td>{user.name}</td>
                        <th>
                            <button class="btn btn-ghost btn-xs">See transactions</button>
                        </th>
                    </tr>
                {/each}
            </tbody>
            <tfoot> </tfoot>
        </table>
    </div>
</div>

<style>
    .user-list {
        height: 40rem;
    }
</style>
