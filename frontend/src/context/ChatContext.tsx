import React, { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import * as chatService from "../services/chatService";
import type {
  ChatMessage,
  ChatContextType,
  GetChatListResponse,
  DeleteChatResponse,
  ProcessQueryResponse,
  ChatList,
} from "../types/chat";

export const ChatContext = createContext<ChatContextType | undefined>(undefined);

export interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [chatList, setChatList] = useState<ChatList[]>([]);
  const [activeChatId, setActiveChatId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMessagesLoading, setIsMessagesLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Retrieves the user's chat list from the backend and updates context state.
   */

  useEffect(() => {
    const handleGetChatList = async (userId: number = 1): Promise<GetChatListResponse> => {
      console.log("Running chat list...")
      setIsLoading(true);
      setError(null);
      try {
        const response = await chatService.getChatList(userId);
        if (response.success && Array.isArray(response.data)) {
          setChatList(response.data);
        }
        return response;
      } catch (err: unknown) {
        const errorMsg = err instanceof Error ? err.message : "Failed to load chat list";
        setError(errorMsg);
        throw err;
      } finally {
        setIsLoading(false);
      }
    };
    handleGetChatList();
  }, []);


  /**
   * Deletes a chat from the backend and updates context state.
   */
  const handleDeleteChat = async (
    chatId: number,
    userId: number = 1
  ): Promise<DeleteChatResponse> => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await chatService.deleteChat(chatId, userId);
      if (response.success) {
        setChatList((prev) =>
          prev.filter((item) => (item.chat_id ?? item.id) !== chatId)
        );
        if (activeChatId === chatId) {
          setActiveChatId(null);
          setMessages([]);
        }
      }
      return response;
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : "Failed to delete chat";
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Sends a user query to the backend processing pipeline.
   */
  const handleProcessQuery = async (
    chatId: number,
    query: string,
    userId: number = 1
  ): Promise<ProcessQueryResponse> => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await chatService.processQuery(chatId, query, userId);
      return response;
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : "Failed to process query";
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Retrieves the individual messages for a specific chat.
   */
  const handleGetChatMessages = async (
    chatId: number | string,
    userId: number = 1
  ): Promise<ChatMessage[]> => {
    setIsMessagesLoading(true);
    setError(null);
    try {
      const fetchedMessages = await chatService.getChatMessages(chatId, userId);
      setMessages(fetchedMessages);
      return fetchedMessages;
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : "Failed to load messages";
      setError(errorMsg);
      throw err;
    } finally {
      setIsMessagesLoading(false);
    }
  };

  const value: ChatContextType = {
    chatList,
    activeChatId,
    messages,
    isLoading,
    isMessagesLoading,
    error,
    setActiveChatId,
    deleteChat: handleDeleteChat,
    processQuery: handleProcessQuery,
    getChatMessages: handleGetChatMessages,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

export function useChat(): ChatContextType {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
}

export default ChatContext;
