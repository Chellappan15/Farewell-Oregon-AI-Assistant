/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import * as chatService from "../services/chatService";
import type {
  ChatList,
  ChatMessage,
  ChatContextType,
} from "../types/chat";
import serverStatus from "../services/serverDetails";

export const ChatContext = createContext<ChatContextType | undefined>(undefined);

export interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const navigate = useNavigate();

  const [chatList, setChatList] = useState<ChatList[]>([]);
  const [activeChatId, setActiveChatId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Centralized Loading States
  const [isChatListLoading, setIsChatListLoading] = useState<boolean>(false);
  const [isMessagesLoading, setIsMessagesLoading] = useState<boolean>(false);
  const [isQueryProcessing, setIsQueryProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [serverStats, setServerStats] = useState<boolean>(false);

  // Server status
  useEffect(() => {
    const fetchServerStatus = async() => {
      const isLive = await serverStatus();
      setServerStats(isLive);
    }

    fetchServerStatus();
  }, []);

  /**
   * 1. Backend-Driven New Chat Creation
   * Calls GET /chat/new-chat, extracts chatId, sets default title "New chat",
   * updates state, and navigates to the dynamic route /chat/:chatId.
   */
  const handleCreateNewChat = async (): Promise<number | null> => {
    setError(null);
    try {
      const response = await chatService.createNewChat(1);
      const newChatId = response.data?.chatId;

      if (newChatId !== undefined && newChatId !== null) {
        const newChatEntry: ChatList = {
          chat_id: newChatId,
          chat_title: "New chat",
          id: newChatId,
        };

        setChatList((prev) => [newChatEntry, ...prev.filter((c) => c.chat_id !== newChatId)]);
        setActiveChatId(newChatId);
        setMessages([]);

        navigate(`/chat/${newChatId}`);
        return newChatId;
      }
      return null;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to create new chat";
      setError(msg);
      console.error(msg, err);
      return null;
    }
  };

  /**
   * 2. Chat Deletion
   * Calls DELETE /chat/delete-chat?user_id=1&chat_id={chatId},
   * removes chat from state, and redirects to / if currently active.
   */
  const handleDeleteChat = async (chatId: number): Promise<boolean> => {
    setError(null);
    try {
      const response = await chatService.deleteChat(chatId, 1);
      if (response.success) {
        setChatList((prev) => prev.filter((item) => item.chat_id !== chatId));

        if (activeChatId === chatId) {
          setActiveChatId(null);
          setMessages([]);
          navigate("/");
        }
        return true;
      }
      return false;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to delete chat";
      setError(msg);
      console.error(msg, err);
      return false;
    }
  };

  /**
   * 3. Chat History (Chat List) Retrieval
   * Calls GET /chat/?user_id=1, exposes isChatListLoading.
   */
  const handleFetchChatList = async (): Promise<ChatList[]> => {
    setIsChatListLoading(true);
    setError(null);
    try {
      const response = await chatService.getChatList(1);
      const list = response.success && Array.isArray(response.data) ? response.data : [];
      setChatList(list);
      return list;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load chat list";
      setError(msg);
      console.error(msg, err);
      return [];
    } finally {
      setIsChatListLoading(false);
    }
  };

  /**
   * 4. Message Retrieval for specific chatId
   * Calls GET /chat/retrieve-messages?user_id=1&chat_id={chatId},
   * exposes isMessagesLoading.
   */
  const handleFetchChatMessages = async (chatId: number): Promise<ChatMessage[]> => {
    setIsMessagesLoading(true);
    setActiveChatId(chatId);
    setError(null);
    try {
      const fetched = await chatService.getChatMessages(chatId, 1);
      setMessages(fetched);
      return fetched;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load messages";
      setError(msg);
      console.error(msg, err);
      setMessages([]);
      return [];
    } finally {
      setIsMessagesLoading(false);
    }
  };

  /**
   * 5. Query Processing
   * Calls POST /{chat_id}?query={query}&user_id=1,
   * handles optimistic updates and exposes isQueryProcessing.
   */
  const handleSendQuery = async (query: string): Promise<void> => {
    const trimmed = query.trim();
    if (!trimmed) return;

    let targetChatId = activeChatId;

    // If no active chat, create one first through the backend
    if (!targetChatId) {
      targetChatId = await handleCreateNewChat();
      console.log(targetChatId);
      if (!targetChatId) return;
    }

    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    const userMessage: ChatMessage = {
      role: "user",
      content: trimmed,
      timestamp,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsQueryProcessing(true);
    setError(null);

    try {
      const response = await chatService.processQuery(targetChatId, trimmed, 1);
      const assistantText = response.data || response.message || "Response received.";

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: assistantText,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // If chat had default title "New chat", update title with query excerpt
      setChatList((prev) =>
        prev.map((c) => {
          if (c.chat_id === targetChatId && (c.chat_title === "New chat" || !c.chat_title)) {
            return {
              ...c,
              chat_title: trimmed.length > 28 ? trimmed.slice(0, 28) + "..." : trimmed,
            };
          }
          return c;
        })
      );
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to process query";
      setError(msg);
      console.error(msg, err);
    } finally {
      setIsQueryProcessing(false);
    }
  };

  const handleClearActiveChat = () => {
    setMessages([]);
  };

  const value: ChatContextType = {
    chatList,
    activeChatId,
    messages,
    isChatListLoading,
    isMessagesLoading,
    isQueryProcessing,
    error,
    serverStatus: serverStats,
    setActiveChatId,
    createNewChat: handleCreateNewChat,
    deleteChat: handleDeleteChat,
    fetchChatList: handleFetchChatList,
    fetchChatMessages: handleFetchChatMessages,
    sendQuery: handleSendQuery,
    clearActiveChat: handleClearActiveChat,
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
