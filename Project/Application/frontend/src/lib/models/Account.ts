import type { UserDetails } from "./UserDetails";

export interface Account {
    id: number;
    userId: number;
    balance: number;
    currency: string;
    user: UserDetails;
}