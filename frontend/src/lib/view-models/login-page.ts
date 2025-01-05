import { goto } from "$app/navigation";
import { UserRole } from "$lib/models/UserRole";
import { userRole } from "$lib/stores/userStore";

export class LoginPage {
    async login(username: string, password: string): Promise<string> {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch("http://localhost:8000/auth/login", {
            method: "POST",
            body: formData,
            credentials: "include",
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Login successful:", data);
            userRole.set(data.user_role);
            localStorage.setItem("role", data.user_role);
            if (data.user_role === UserRole.USER) {
                await goto("/home");
                return "";
            }

            await goto("/admin");
            return "";
        } else {
            console.error("Login failed:", response.statusText);
            const data = await response.json();
            return data.detail;
        }
    }
}