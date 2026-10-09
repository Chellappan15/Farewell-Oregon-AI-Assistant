import apiClient from "./api";
import type {
  GetChatListResponse,
  DeleteChatResponse,
  ProcessQueryResponse,
  NewChatResponse,
  ChatMessage,
} from "../types/chat";

/**
 * 1. Creates a new chat on the backend.
 * Endpoint: GET /chat/new-chat
 */
export async function createNewChat(userId: number = 1): Promise<NewChatResponse> {
  try {
    const response = await apiClient.get<NewChatResponse>("/chat/new-chat", {
      params: { user_id: userId },
    });
    return response.data;
  } catch (error) {
    console.error("Failed to create new chat:", error);
    throw error;
  }
}

/**
 * 2. Deletes a specific chat by ID for a user.
 * Endpoint: DELETE /chat/delete-chat?user_id={userId}&chat_id={chatId}
 */
export async function deleteChat(
  chatId: number,
  userId: number = 1
): Promise<DeleteChatResponse> {
  try {
    const response = await apiClient.delete<DeleteChatResponse>("/chat/delete-chat", {
      params: {
        user_id: userId,
        chat_id: chatId,
      },
    });
    return response.data;
  } catch (error) {
    console.error(`Failed to delete chat ${chatId}:`, error);
    throw error;
  }
}

/**
 * 3. Retrieves the message history for a specific chat.
 * Endpoint: GET /chat/retrieve-messages?user_id={userId}&chat_id={chatId}
 */
export async function getChatMessages(
  chatId: number,
  userId: number = 1
): Promise<ChatMessage[]> {
  try {
    const response = await apiClient.get<{
      data?: unknown[];
      messages?: unknown[];
      success?: boolean;
    }>("/chat/retrieve-messages", {
      params: {
        user_id: userId,
        chat_id: chatId,
      },
    });

    const rawList =
      response.data?.data ||
      response.data?.messages ||
      (Array.isArray(response.data) ? response.data : []);
    console.log("Message data: ", rawList);

    // Transform backend message formats ({ role, parts: [{text}], time_stamp }) to ChatMessage
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
    console.error(`Failed to fetch messages for chat ${chatId}:`, error);
    throw error;
  }
}

/**
 * 4. Sends a query/message to the backend to process via LLM + RAG + Tools.
 * Endpoint: POST /{chat_id}?query={query}
 */
export async function processQuery(
  chatId: number,
  query: string,
  userId: number = 1
): Promise<ProcessQueryResponse> {
  try {
    const response = await apiClient.post<ProcessQueryResponse>(
      `/${chatId}`,
      null,
      {
        params: {
          query,
          user_id: userId,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error(`Failed to process query for chat ${chatId}:`, error);
    throw error;
  }
}

/**
 * 5. Retrieves the list of available chats for a user from the backend.
 * Endpoint: GET /chat/?user_id={userId}
 */
export async function getChatList(userId: number = 1): Promise<GetChatListResponse> {
  try {
    const response = await apiClient.get<GetChatListResponse>("/chat/", {
      params: { user_id: userId },
    });
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
  getChatList,
};
