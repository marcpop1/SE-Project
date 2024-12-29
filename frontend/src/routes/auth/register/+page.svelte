<script lang="ts">
  let username: string = "";
  let password: string = "";
  let confirmPassword: string = "";
  let isPasswordMatch: boolean = true;
  let noMatchErrorMessage: string = "Passwords do not match";
  
  $: isPasswordMatch = password === confirmPassword ? true : false;

  async function handleSubmit(event: any) {
    if (!isPasswordMatch) {
      return;
    }

    event.preventDefault();

    const response = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, password: password }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log("Login successful:", data);
    } else {
      console.error("Login failed:", response.statusText);
    }
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
            id="emaiusernamel"
            autocomplete="username"
            bind:value={username}
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
            autocomplete="current-password"
            bind:value={password}
            required
            class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
          />
        </div>
      </div>
      <div>
        <div class="flex items-center justify-between">
          <label
            for="confirm-password"
            class="block text-sm/6 font-medium text-gray-900"
            >Confirm password</label
          >
          {#if isPasswordMatch === false}
          <div class="text-sm">
            <span class="font-semibold text-red-600 hover:text-red-500">{noMatchErrorMessage}</span>
          </div>
          {/if}
        </div>
        <div class="mt-2">
          <input
            type="password"
            name="password"
            id="confirm-password"
            autocomplete="current-password"
            bind:value={confirmPassword}
            required
            class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
          />
        </div>
      </div>

      <div>
        <button
          type="submit"
          class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >Sign up</button
        >
      </div>

      <p class="text-sm font-light text-gray-500 dark:text-gray-400">
        Already have an account? <a href="/auth/login" class="font-medium text-indigo-600 hover:underline dark:text-primary-500">Sign in</a>
    </p>
    </form>
  </div>
</div>
