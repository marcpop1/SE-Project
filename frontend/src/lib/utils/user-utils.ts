import { goto } from "$app/navigation";

export class UserUtils {
    async logout() {
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
            localStorage.removeItem('role');
            goto("/auth/login");
        } catch (error) {
            console.error("Failed to logout:", error);
        }
    }
}