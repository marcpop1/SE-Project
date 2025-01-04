import type { CardType } from "./CardType";

export interface Card {
    id: number;
    accountId: number;
    holderName: string;
    number: string;
    expirationMonth: number;
    expirationYear: number;
    cvv: string;
    type: CardType;
    currency: string;
}