import React, { useEffect, useRef } from "react";
import { Crosshair, ShieldAlert, Zap, Skull, Loader2 } from "lucide-react";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import { useChat } from "../../context/ChatContext";

const SUGGESTED_PROMPTS = [
  {
    icon: <Skull size={16} />,
    title: "Breaker Strategy",
    prompt: "What is the best tactical strategy to eliminate a Breaker Freaker?",
  },
  {
    icon: <Crosshair size={16} />,
    title: "Weapon Comparison",
    prompt: "Compare the SAF rifle and the MWS. Which is better for early-to-mid game?",
  },
  {
    icon: <ShieldAlert size={16} />,
    title: "Horde Survival",
    prompt: "What gear and loadout do I need to take on the Iron Butte Horde?",
  },
  {
    icon: <Zap size={16} />,
    title: "Crafting Intel",
    prompt: "Where can I reliably scavenge Kerosene and Nest Residue for Incendiary Bolts?",
  },
];

export const MessageList: React.FC = () => {
  const { messages, isMessagesLoading, isQueryProcessing, sendQuery } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isQueryProcessing, isMessagesLoading]);

  // 1. If messages are currently loading from endpoint, display the tactical loader
  if (isMessagesLoading) {
    return (
      <div className="messages-loading-state">
        <div className="messages-loading-spinner-wrap">
          <Loader2 size={38} className="messages-spinner" />
        </div>
        <h3 className="loading-state-title">Retrieving Tactical Logs...</h3>
        <p className="loading-state-desc">
          Querying Days Gone conversation archive for selected briefing.
        </p>
      </div>
    );
  }

  // 2. If no messages are loaded for this chat, show prompt suggestions
  if (!messages || messages.length === 0) {
    return (
      <div className="empty-chat-state">
        <div className="empty-hero-icon">
          <Crosshair size={36} />
        </div>

        <h2 className="empty-title">Days Gone Survival Intelligence</h2>
        <p className="empty-subtitle">
          DevMind AI assists survivors with Freaker combat tactics, horde pathing,
          weapon stats, and Oregon wasteland survival strategies.
        </p>

        <div className="suggested-prompts-grid">
          {SUGGESTED_PROMPTS.map((item, idx) => (
            <button
              key={idx}
              type="button"
              className="prompt-card"
              onClick={() => sendQuery(item.prompt)}
            >
              <div className="prompt-card-header">
                <span className="prompt-card-icon">{item.icon}</span>
                <span className="prompt-card-title">{item.title}</span>
              </div>
              <p className="prompt-card-body">{item.prompt}</p>
            </button>
          ))}
        </div>
      </div>
    );
  }

  // 3. Messages loaded from history/chat: render the message list
  return (
    <div className="message-list-container">
      {messages.map((msg, idx) => (
        <MessageBubble
          key={`${msg.role}-${idx}-${msg.timestamp ?? ""}`}
          message={msg}
        />
      ))}

      {isQueryProcessing && <TypingIndicator />}

      <div ref={bottomRef} className="scroll-anchor" />
    </div>
  );
};

export default MessageList;
