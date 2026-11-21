import type { GameKey } from "../types/chat";

export type PromptIcon = "skull" | "crosshair" | "shield" | "zap" | "user" | "map" | "tag" | "gauge";

export interface GameProfile {
  key: GameKey;
  label: string;
  description: string;
  title: string;
  subtitle: string;
  assistantName: string;
  playerLabel: string;
  placeholder: string;
  emptyTitle: string;
  emptySubtitle: string;
  knowledgeSummary: string;
  tools: string[];
  prompts: { icon: PromptIcon; title: string; prompt: string }[];
}

export const GAME_PROFILES: Record<GameKey, GameProfile> = {
  days_gone: {
    key: "days_gone",
    label: "Days Gone",
    description: "Freakers, hordes, weapons and survival in Farewell, Oregon",
    title: "Days Gone Assistant",
    subtitle: "Survival intelligence for Days Gone",
    assistantName: "Farewell Oregon AI",
    playerLabel: "Survivor (Player)",
    placeholder: "Ask anything about Days Gone...",
    emptyTitle: "Days Gone Survival Intelligence",
    emptySubtitle:
      "Farewell Oregon AI assists survivors with Freaker combat tactics, horde pathing, weapon stats, and Oregon wasteland survival strategies.",
    knowledgeSummary: "ChromaDB vector database indexed with Days Gone weapons, Freakers, and tactical survival lore.",
    tools: ["compare_weapons", "zombie_details"],
    prompts: [
      { icon: "skull", title: "Breaker Strategy", prompt: "What is the best tactical strategy to eliminate a Breaker Freaker?" },
      { icon: "crosshair", title: "Weapon Comparison", prompt: "Compare the SAF rifle and the MWS. Which is better for early-to-mid game?" },
      { icon: "shield", title: "Horde Survival", prompt: "What gear and loadout do I need to take on the Iron Butte Horde?" },
      { icon: "zap", title: "Crafting Intel", prompt: "Where can I reliably scavenge Kerosene and Nest Residue for Incendiary Bolts?" },
    ],
  },
  gta6: {
    key: "gta6",
    label: "GTA 6",
    description: "Jason, Lucia, Vice City and the state of Leonida",
    title: "GTA 6 Assistant",
    subtitle: "Street intelligence for Grand Theft Auto VI",
    assistantName: "Leonida AI",
    playerLabel: "Player",
    placeholder: "Ask anything about GTA 6...",
    emptyTitle: "GTA 6 Leonida Intelligence",
    emptySubtitle:
      "Leonida AI answers questions about Jason and Lucia, Vice City and the rest of Leonida, editions, gameplay systems and launch facts.",
    knowledgeSummary: "ChromaDB vector database indexed with GTA 6 characters, Leonida regions, editions and gameplay systems.",
    tools: ["get_character", "get_region", "compare_editions", "get_game_facts"],
    prompts: [
      { icon: "user", title: "Meet the Cast", prompt: "Who is Lucia Caminos and how is she connected to Jason?" },
      { icon: "map", title: "Explore Leonida", prompt: "What is Port Gellhorn like and what real place is it based on?" },
      { icon: "tag", title: "Pick an Edition", prompt: "What do I get with the Ultimate Edition compared to the Standard Edition?" },
      { icon: "gauge", title: "Performance", prompt: "Does GTA 6 run at 60 fps on the PS5 Pro?" },
    ],
  },
};

export const GAME_OPTIONS: GameProfile[] = [GAME_PROFILES.days_gone, GAME_PROFILES.gta6];

export function getGameProfile(game: GameKey): GameProfile {
  return GAME_PROFILES[game] ?? GAME_PROFILES.days_gone;
}
