/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import * as chatService from "../services/chatService";
import type {
  ChatList,
  ChatMessage,
  ChatContextType,
  ErrorInterface,
  RetrievalMode,
  GameKey,
} from "../types/chat";
import serverStatus from "../services/serverDetails";
import { useAuth } from "./AuthContext";

export const ChatContext = createContext<ChatContextType | undefined>(undefined);

export interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  const [chatList, setChatList] = useState<ChatList[]>([]);
  const [activeChatId, setActiveChatId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Centralized Loading States
  const [isChatListLoading, setIsChatListLoading] = useState<boolean>(false);
  const [isMessagesLoading, setIsMessagesLoading] = useState<boolean>(false);
  const [isQueryProcessing, setIsQueryProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [serverStats, setServerStats] = useState<boolean>(false);

  // Retrieval mode chosen in the input box (remembered across reloads)
  const [retrievalMode, setRetrievalModeState] = useState<RetrievalMode>(() => {
    const saved = localStorage.getItem("dg_retrieval_mode");
    return saved === "dense" || saved === "text" || saved === "hybrid" ? saved : "hybrid";
  });

  const setRetrievalMode = (mode: RetrievalMode) => {
    setRetrievalModeState(mode);
    localStorage.setItem("dg_retrieval_mode", mode);
  };

  // Game chosen in the input box (remembered across reloads)
  const [game, setGameState] = useState<GameKey>(() => {
    const saved = localStorage.getItem("dg_game");
    return saved === "gta6" || saved === "days_gone" ? saved : "days_gone";
  });

  const setGame = (next: GameKey) => {
    setGameState(next);
    localStorage.setItem("dg_game", next);
  };

  // Server status
  useEffect(() => {
    const fetchServerStatus = async() => {
      const isLive = await serverStatus();
      setServerStats(isLive);
    }

    fetchServerStatus();
  }, []);


  // Handler for new chat creation
  const handleCreateNewChat = async (): Promise<number | null> => {
    setError(null);
    try {
      const response = await chatService.createNewChat();
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

  // Handler for chat deletion
  const handleDeleteChat = async (chatId: number): Promise<boolean> => {
    setError(null);
    try {
      const response = await chatService.deleteChat(chatId);
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

  // Chat list history retrieval
  const handleFetchChatList = async (): Promise<ChatList[]> => {
    setIsChatListLoading(true);
    setError(null);
    try {
      const response = await chatService.getChatList();
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


  // Chat history retrieval
  const handleFetchChatMessages = async (
    chatId: number
  ): Promise<ErrorInterface | ChatMessage[] > => {
    setIsMessagesLoading(true);
    setActiveChatId(chatId);
    setError(null);

    try {
      const fetched = await chatService.getChatMessages(chatId);

      console.log("Fetched response:", fetched);
      console.log("Is array:", Array.isArray(fetched));
      console.log("Current path:", window.location.pathname);
      if (Array.isArray(fetched)) {
        setMessages(fetched);
        return fetched;
      }

      if (!fetched.success) {
        navigate("/", {
          replace: true
        });
        return fetched;
      }

      return fetched;
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Failed to load messages";

      setError(msg);
      console.error(msg, err);
      setMessages([]);

      return [];
    } finally {
      setIsMessagesLoading(false);
    }
  };

  // Query processing handlers
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

    const userMessage: ChatMessage = {
      role: "user",
      content: trimmed,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsQueryProcessing(true);
    setError(null);

    try {
      let hasStarted = false;
      await chatService.processQueryStream(targetChatId, trimmed, (chunk) => {
        const isFirstChunk = !hasStarted;
        hasStarted = true;
        setMessages((prev) => {
          // First chunk adds the assistant message, later chunks append to it
          if (isFirstChunk) {
            return [...prev, { role: "assistant", content: chunk }];
          }
          const last = prev[prev.length - 1];
          return [...prev.slice(0, -1), { ...last, content: last.content + chunk }];
        });
      }, retrievalMode, game);

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

  // const handleClearActiveChat = () => {
  //   setMessages([]);
  // };

  // When auth state changes, reload chat list or reset state
  useEffect(() => {
    const authenticateUser = () => {
      if (isAuthenticated && user?.id) {
        handleFetchChatList();
      } else if (!isAuthenticated) {
        setChatList([]);
        setMessages([]);
        setActiveChatId(null);
      }
    }

    authenticateUser();
  }, [isAuthenticated, user?.id]);

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
    retrievalMode,
    setRetrievalMode,
    game,
    setGame,
    // clearActiveChat: handleClearActiveChat,
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
