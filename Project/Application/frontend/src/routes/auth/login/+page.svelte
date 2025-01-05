<script lang="ts">
  import { LoginPage } from "$lib/view-models/login-page";

  let username: string = "";
  let password: string = "";
  let errorMessage: string = "";

  const loginPage = new LoginPage();

  async function handleSubmit(event: any) {
    event.preventDefault();

    errorMessage = await loginPage.login(username, password);
  }
</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
  <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
    <form class="space-y-6" method="POST" on:submit={handleSubmit}>
      <div>
        <label for="username" class="block text-sm/6 font-medium text-gray-900"
          >Username</label
        >
        <div class="mt-2">
          <input
            type="username"
            name="username"
            id="username"
            bind:value={username}
            autocomplete="username"
            required
            class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
          />
        </div>
      </div>

      <div>
        <div class="flex items-center justify-between">
          <label
            for="password"
            class="block text-sm/6 font-medium text-gray-900">Password</label
          >
        </div>
        <div class="mt-2">
          <input
            type="password"
            name="password"
            id="password"
            bind:value={password}
            autocomplete="current-password"
            required
            class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
          />
        </div>
      </div>
      <div class="text-center">
        {#if errorMessage}
          <span class="text-red-600">{errorMessage}</span>
        {/if}
      </div>
      <div>
        <button
          type="submit"
          class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >Sign in</button
        >
      </div>

      <p class="text-sm font-light text-gray-500 dark:text-gray-400">
        Don’t have an account yet? <a
          href="/auth/register"
          class="font-medium text-indigo-600 hover:underline dark:text-primary-500"
          >Sign up</a
        >
      </p>
    </form>
  </div>
</div>
