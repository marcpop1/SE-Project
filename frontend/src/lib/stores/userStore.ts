import { goto } from '$app/navigation';
import { writable } from 'svelte/store';

export const userRole = writable<string | null>(null);

export async function logout() {
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