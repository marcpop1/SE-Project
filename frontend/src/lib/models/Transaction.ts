export interface Transaction {
    id: number;
    accountFromId: number;
    accountToId: number;
    amount: number;
    currency: string;
    createdAt: Date;
}