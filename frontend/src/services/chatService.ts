import apiClient from "./api";
import type {
  GetChatListResponse,
  DeleteChatResponse,
  ProcessQueryResponse,
  NewChatResponse,
  ChatMessage,
  ErrorInterface
} from "../types/chat";

// Chat creation
export async function createNewChat(): Promise<NewChatResponse> {
  try {
    const response = await apiClient.get<NewChatResponse>("/chat/new-chat");
    return response.data;
  } catch (error) {
    console.error("Failed to create new chat:", error);
    throw error;
  }
}

// Chat deletion
export async function deleteChat(chatId: number): Promise<DeleteChatResponse> {
  try {
    const response = await apiClient.delete<DeleteChatResponse>("/chat/delete-chat", {
      params: {
        chat_id: chatId,
      },
    });
    return response.data;
  } catch (error) {
    console.error(`Failed to delete chat ${chatId}:`, error);
    throw error;
  }
}

// Retrieve chat messages
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

// Query processing
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

// Get the chat list
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
  getChatList,
};
