import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Gamepad2,
  Plus,
  Search,
  MessageSquare,
  Settings,
  User,
  X,
  Trash2,
  Loader2,
  LogOut,
} from "lucide-react";
import { useChat } from "../../context/ChatContext";
import { useAuth } from "../../context/AuthContext";
import IconButton from "../common/IconButton";

export interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpen = true,
  onClose,
}) => {
  const navigate = useNavigate();
  const {
    chatList,
    activeChatId,
    isChatListLoading,
    createNewChat,
    deleteChat,
  } = useChat();

  const { user, logout } = useAuth();
  const [searchQuery, setSearchQuery] = useState("");

  const filteredConversations = chatList.filter((c) =>
    (c.chat_title || "").toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSelectChat = (chatId: number) => {
    navigate(`/chat/${chatId}`);
    if (onClose) onClose();
  };

  const handleNewChatClick = async () => {
    await createNewChat();
    if (onClose) onClose();
  };

  const handleLogoutClick = () => {
    logout();
    navigate("/login");
  };

  return (
    <>
      {/* Mobile backdrop */}
      <div
        className={`sidebar-backdrop ${isOpen ? "open" : ""}`}
        onClick={onClose}
        aria-hidden="true"
      />

      <aside className={`sidebar ${isOpen ? "open" : ""}`}>
        {/* Logo / Brand Header */}
        <div className="sidebar-logo">
          <div className="logo-icon">
            <Gamepad2 size={22} className="logo-gamepad" />
          </div>

          <div className="logo-text">
            <h2>DevMind</h2>
            <span>Gaming Intelligence</span>
          </div>

          {onClose && (
            <IconButton
              icon={<X size={18} />}
              label="Close Sidebar"
              size="sm"
              onClick={onClose}
              className="sidebar-close-mobile"
            />
          )}
        </div>

        {/* New Chat Button */}
        <button
          type="button"
          className="new-chat-button"
          onClick={handleNewChatClick}
        >
          <Plus size={18} />
          <span>New Chat</span>
        </button>

        {/* Search */}
        <div className="chat-search">
          <Search size={16} className="search-icon" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search chats..."
            aria-label="Search chats"
          />
          {searchQuery && (
            <button
              type="button"
              className="search-clear-btn"
              onClick={() => setSearchQuery("")}
            >
              <X size={13} />
            </button>
          )}
        </div>

        {/* Recent Chats Section */}
        <div className="recent-section">
          <p className="section-title">RECENT CONVERSATIONS</p>

          <div className="recent-list">
            {isChatListLoading ? (
              <div className="sidebar-loading-state">
                <Loader2 size={16} className="sidebar-spinner" />
                <span>Loading chats...</span>
              </div>
            ) : filteredConversations.length > 0 ? (
              filteredConversations.map((conv) => {
                const isActive = conv.chat_id === activeChatId;
                return (
                  <div
                    key={conv.chat_id}
                    className={`chat-item ${isActive ? "active" : ""}`}
                    onClick={() => handleSelectChat(conv.chat_id)}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        handleSelectChat(conv.chat_id);
                      }
                    }}
                  >
                    <MessageSquare size={16} className="chat-item-icon" />
                    <span className="chat-item-title" title={conv.chat_title}>
                      {conv.chat_title}
                    </span>

                    <button
                      type="button"
                      className="chat-item-delete"
                      title="Delete chat"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteChat(conv.chat_id);
                      }}
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                );
              })
            ) : (
              <div className="no-chats-found">
                <span>{searchQuery ? "No matching chats" : "No recent chats"}</span>
              </div>
            )}
          </div>
        </div>

        {/* Bottom Section */}
        <div className="sidebar-bottom">
          <button type="button" className="sidebar-button">
            <Settings size={18} />
            <span>Settings</span>
          </button>

          <div className="user-profile">
            <div className="user-avatar">
              <User size={18} />
            </div>

            <div className="user-info">
              <strong title={user?.name || user?.email || "Player"}>
                {user?.name || user?.email?.split("@")[0] || "Player"}
              </strong>
              <span title={user?.email || "Survivor"}>
                {user?.email || "Survivor • Lv. 32"}
              </span>
            </div>

            <button
              type="button"
              className="logout-button"
              title="Logout from terminal"
              aria-label="Logout"
              onClick={handleLogoutClick}
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;