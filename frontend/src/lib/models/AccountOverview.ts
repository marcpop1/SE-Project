import type { Account } from "./Account";
import type { Card } from "./Card";
import type { Transaction } from "./Transaction";
import type { UserDetails } from "./UserDetails";

export interface AccountOverview {
    user: UserDetails;
    account: Account;
    cards: Card[];
    transactions: Transaction[];
}