import React, { useEffect, useRef } from "react";
import { Crosshair, ShieldAlert, Zap, Skull, Loader2, UserRound, MapPin, Tag, Gauge } from "lucide-react";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import { useChat } from "../../context/ChatContext";
import { getGameProfile, type PromptIcon } from "../../utils/games";

const PROMPT_ICONS: Record<PromptIcon, React.ReactNode> = {
  skull: <Skull size={16} />,
  crosshair: <Crosshair size={16} />,
  shield: <ShieldAlert size={16} />,
  zap: <Zap size={16} />,
  user: <UserRound size={16} />,
  map: <MapPin size={16} />,
  tag: <Tag size={16} />,
  gauge: <Gauge size={16} />,
};

export const MessageList: React.FC = () => {
  const { messages, isMessagesLoading, isQueryProcessing, sendQuery, game } = useChat();
  const profile = getGameProfile(game);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isQueryProcessing, isMessagesLoading]);

  if (isMessagesLoading) {
    return (
      <div className="messages-loading-state">
        <div className="messages-loading-spinner-wrap">
          <Loader2 size={38} className="messages-spinner" />
        </div>
        <h3 className="loading-state-title">Retrieving Tactical Logs...</h3>
        <p className="loading-state-desc">
          Querying {profile.label} conversation archive for selected briefing.
        </p>
      </div>
    );
  }

  if (!messages || messages.length === 0) {
    return (
      <div className="empty-chat-state">
        <div className="empty-hero-icon">
          <Crosshair size={36} />
        </div>

        <h2 className="empty-title">{profile.emptyTitle}</h2>
        <p className="empty-subtitle">{profile.emptySubtitle}</p>

        <div className="suggested-prompts-grid">
          {profile.prompts.map((item, idx) => (
            <button
              key={idx}
              type="button"
              className="prompt-card"
              onClick={() => sendQuery(item.prompt)}
            >
              <div className="prompt-card-header">
                <span className="prompt-card-icon">{PROMPT_ICONS[item.icon]}</span>
                <span className="prompt-card-title">{item.title}</span>
              </div>
              <p className="prompt-card-body">{item.prompt}</p>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="message-list-container">
      {messages.map((msg, idx) => (
        <MessageBubble
          key={`${msg.role}-${idx}-${msg.timestamp ?? ""}`}
          message={msg}
        />
      ))}

      {isQueryProcessing && messages[messages.length - 1]?.role !== "assistant" && <TypingIndicator />}

      <div ref={bottomRef} className="scroll-anchor" />
    </div>
  );
};

export default MessageList;
