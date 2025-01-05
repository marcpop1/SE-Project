import { goto } from "$app/navigation";

export class RegisterPage {
    async register(name: string, username: string, password: string) {
        const response = await fetch("http://localhost:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: name, username: username, password: password }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Login successful:", data);
            await goto("/auth/login");
        } else {
            console.error("Login failed:", response.statusText);
        }
    }
}