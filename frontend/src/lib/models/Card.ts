export interface Card {
    id: number;
    accountId: number;
    holderName: string;
    number: string;
    expirationMonth: number;
    expirationYear: number;
    cvv: string;
    type: string;
    currency: string;
    isPrimary: boolean;
}