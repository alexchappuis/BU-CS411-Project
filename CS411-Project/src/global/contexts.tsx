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

interface GamesCon {
    games: Game[];
    setGames: (u: Game[]) => void;
}

export const SteamContext = createContext<GamesCon>({
    games: [],
    setGames: (gs: Game[]) => {}
})

export interface Song {
    name: string;
    id: string;
    duration: number;
    coverUrl: string;
    previewUrl: string;
}

interface PlayListCon {
    playlist: Song[];
    setPlaylist: (pl: Song[]) => void;
}

export const PlaylistContext = createContext<PlayListCon>({
    playlist: [],
    setPlaylist: (pl: Song[]) => {}
})