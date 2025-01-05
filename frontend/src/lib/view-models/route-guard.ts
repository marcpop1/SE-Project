import { goto } from "$app/navigation";
import { UserRole } from "$lib/models/UserRole";
import { userRole } from "$lib/stores/user-store";
import type { Page } from "@sveltejs/kit";

export class RouteGuard {
    async checkRouteAccess(page: Page<Record<string, string>, string | null>) {
        const role = localStorage.getItem("role");
		console.log("after navigate " + role);
		if (role) {
			userRole.set(role);
		} else {
			userRole.set(null);
		}

		if (page.url.pathname === "/") {
			await goto("/auth/login");
			return;
		}
		else if (page.url.pathname.startsWith("/auth") && role) {
			if (role === UserRole.ADMIN) {
				await goto("/admin");
				return;
			}

			await goto("/home");
			return;
		}
		else if (!page.url.pathname.startsWith("/admin") && role === UserRole.ADMIN) {
			await goto("/admin");
			return;
		}
		else if (page.url.pathname.startsWith("/admin") && role !== UserRole.ADMIN) {
			await goto("/home");
			return;
		}
    }
}