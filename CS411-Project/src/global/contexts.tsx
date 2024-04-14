import { createContext } from "react"

export const TokenContext = createContext({
    token: "",
    setToken: (t: string) => {}
})

export interface Game {
    id: number;
    name: string;
    playtime: number;
    iconUrl: string;
    logoUrl: string;
    rank: number;
}

export interface User {
    name: string;
    id: number;
    games: Game[];
}

interface UserCon {
    user: User;
    setUser: (u: User) => void;
}

export const SteamContext = createContext<UserCon>({
    user: {name: "", id: -1, games: []},
    setUser: (u: User) => {}
})