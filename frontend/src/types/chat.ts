export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  role: MessageRole;
  content: string;
  timestamp?: string;
}

export interface Conversation {
  id: string;
  title: string;
  lastUpdated: string;
  messages: ChatMessage[];
}

export type SubsystemStatus = "ready" | "active" | "standby" | "operational";

export interface AISubsystem {
  id: string;
  name: string;
  category: "RAG" | "Memory" | "Tools" | "Agent";
  status: SubsystemStatus;
  detail: string;
  stats?: string;
}

// --- Backend API Integration Types ---

export interface ChatList {
  chat_id?: number;
  chat_title: string;
  id?: number;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
}

export type GetChatListResponse = ApiResponse<ChatList[]>;

export type DeleteChatResponse = ApiResponse<never>;

export type ProcessQueryResponse = ApiResponse<string>;

export type GetChatMessagesResponse = ApiResponse<ChatMessage[]>;

export interface ChatContextType {
  chatList: ChatList[];
  activeChatId: number | null;
  messages: ChatMessage[];
  isLoading: boolean;
  isMessagesLoading: boolean;
  error: string | null;
  setActiveChatId: (id: number | null) => void;
  deleteChat: (chatId: number, userId?: number) => Promise<DeleteChatResponse>;
  processQuery: (chatId: number, query: string, userId?: number) => Promise<ProcessQueryResponse>;
  getChatMessages: (chatId: number | string, userId?: number) => Promise<ChatMessage[]>;
}
