import axios from "axios";
import apiClient, { API_BASE_URL } from "./api";
import type {
  GetChatListResponse,
  DeleteChatResponse,
  ProcessQueryResponse,
  NewChatResponse,
  ChatMessage,
  ErrorInterface,
  RetrievalMode,
  GameKey
} from "../types/chat";

export async function createNewChat(): Promise<NewChatResponse> {
  try {
    const response = await apiClient.post<NewChatResponse>("/chat/new-chat");
    return response.data;
  } catch (error) {
    console.error("Failed to create new chat:", error);
    throw error;
  }
}

export async function deleteChat(chatId: number): Promise<DeleteChatResponse> {
  try {
    const response = await apiClient.delete<DeleteChatResponse>("/chat/delete-chat", {
      params: {
        chat_id: chatId,
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return error.response.data as DeleteChatResponse;
    }
    console.error(`Failed to delete chat ${chatId}:`, error);
    throw error;
  }
}

export async function getChatMessages(chatId: number): Promise<ChatMessage[] | ErrorInterface> {
  try {
    const response = await apiClient.get<{
      data?: unknown[];
      message?: string;
      success?: boolean;
    }>("/chat/retrieve-messages", {
      params: {
        chat_id: chatId,
      },
    });

    if (response.status == 200 && !response?.data?.success) {
      return {
        success: response.data.success ?? false,
        message: response.data.message ?? "Error retrieving data."
      }
    }

    const rawList =
      response.data?.data ||
      (Array.isArray(response.data) ? response.data : []);
    console.log("Message data: ", rawList);

    return (rawList as Record<string, unknown>[]).map((item) => {
      let content = "";
      if (typeof item.content === "string") {
        content = item.content;
      } else if (Array.isArray(item.parts) && item.parts.length > 0) {
        content = item.parts.map((p: { text?: string }) => p?.text || "").join("");
      } else if (typeof item.text === "string") {
        content = item.text;
      }

      const role =
        item.role === "model" || item.role === "assistant" ? "assistant" : "user";
      const timestamp =
        (item.time_stamp as string) || (item.timestamp as string) || undefined;

      return {
        role,
        content,
        timestamp,
      };
    });
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return {
        success: false,
        message: error.response.data?.message ?? "Chat is not available",
      };
    }
    console.error(`Failed to fetch messages for chat ${chatId}:`, error);
    throw error;
  }
}

export async function processQuery(
  chatId: number,
  query: string,
  retrievalMode: RetrievalMode = "hybrid",
  game: GameKey = "days_gone"
): Promise<ProcessQueryResponse> {
  try {
    const response = await apiClient.post<ProcessQueryResponse>(
      `/chat/${chatId}`,
      { query, retrieval_mode: retrievalMode, game }
    );
    return response.data;
  } catch (error) {
    console.error(`Failed to process query for chat ${chatId}:`, error);
    throw error;
  }
}

export async function processQueryStream(
  chatId: number,
  query: string,
  onChunk: (chunk: string) => void,
  retrievalMode: RetrievalMode = "hybrid",
  game: GameKey = "days_gone"
): Promise<string> {
  try {
    const token = localStorage.getItem("dg_auth_token");
    const url = `${API_BASE_URL}/chat/${chatId}/stream`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ query, retrieval_mode: retrievalMode, game }),
    });

    if (!response.ok || !response.body) {
      throw new Error(`Stream request failed with status ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      if (chunk) {
        fullText += chunk;
        onChunk(chunk);
      }
    }

    return fullText;
  } catch (error) {
    console.error(`Failed to stream query for chat ${chatId}:`, error);
    throw error;
  }
}

export async function getChatList(): Promise<GetChatListResponse> {
  try {
    const response = await apiClient.get<GetChatListResponse>("/chat/");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch chat list:", error);
    throw error;
  }
}

export default {
  createNewChat,
  deleteChat,
  getChatMessages,
  processQuery,
  processQueryStream,
  getChatList,
};
