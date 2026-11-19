import React, { useState, useRef, useEffect } from "react";
import { Send, CornerDownLeft, Layers, ChevronUp, Check } from "lucide-react";
import { useChat } from "../../context/ChatContext";
import type { RetrievalMode } from "../../types/chat";

const RETRIEVAL_OPTIONS: { value: RetrievalMode; label: string; description: string }[] = [
  { value: "hybrid", label: "Hybrid", description: "Vector + BM25, fused and reranked" },
  { value: "dense", label: "Dense", description: "Vector (semantic) search only" },
  { value: "text", label: "Text", description: "BM25 keyword search only" },
];

export interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
}) => {
  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { retrievalMode, setRetrievalMode } = useChat();
  const [isModeMenuOpen, setIsModeMenuOpen] = useState(false);
  const modeMenuRef = useRef<HTMLDivElement>(null);

  // Close the retrieval menu when clicking outside it
  useEffect(() => {
    if (!isModeMenuOpen) return;
    const handleClickOutside = (e: MouseEvent) => {
      if (modeMenuRef.current && !modeMenuRef.current.contains(e.target as Node)) {
        setIsModeMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isModeMenuOpen]);

  const activeOption =
    RETRIEVAL_OPTIONS.find((option) => option.value === retrievalMode) ?? RETRIEVAL_OPTIONS[0];

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "auto";
    const nextHeight = Math.min(textarea.scrollHeight, 180);
    textarea.style.height = `${nextHeight}px`;
  }, [text]);

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;

    onSendMessage(trimmed);
    setText("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="chat-input-wrapper">
      <div className={`chat-input-container ${disabled ? "input-disabled" : ""}`}>
        <div className="retrieval-mode" ref={modeMenuRef}>
          <button
            type="button"
            onClick={() => setIsModeMenuOpen((open) => !open)}
            disabled={disabled}
            className="retrieval-mode-button"
            aria-haspopup="listbox"
            aria-expanded={isModeMenuOpen}
            title={`Retrieval: ${activeOption.label}`}
          >
            <Layers size={14} />
            <span>{activeOption.label}</span>
            <ChevronUp size={12} />
          </button>

          {isModeMenuOpen && (
            <ul className="retrieval-mode-menu" role="listbox">
              {RETRIEVAL_OPTIONS.map((option) => (
                <li key={option.value}>
                  <button
                    type="button"
                    role="option"
                    aria-selected={option.value === retrievalMode}
                    className={`retrieval-mode-option ${option.value === retrievalMode ? "active" : ""}`}
                    onClick={() => {
                      setRetrievalMode(option.value);
                      setIsModeMenuOpen(false);
                    }}
                  >
                    <span className="retrieval-mode-option-text">
                      <span className="retrieval-mode-option-label">{option.label}</span>
                      <span className="retrieval-mode-option-desc">{option.description}</span>
                    </span>
                    {option.value === retrievalMode && <Check size={14} />}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about Days Gone..."
          disabled={disabled}
          rows={1}
          className="chat-textarea"
        />

        <button
          type="button"
          onClick={handleSubmit}
          disabled={!text.trim() || disabled}
          className="chat-send-button"
          aria-label="Send message"
          title="Send (Enter)"
        >
          <Send size={16} />
        </button>
      </div>

      <div className="chat-input-footer">
        <span className="chat-input-hint">
          Farewell Oregon AI can use game knowledge, conversation memory and tools.
        </span>
        <span className="chat-input-shortcut">
          <CornerDownLeft size={11} /> Enter to send • Shift+Enter for newline
        </span>
      </div>
    </div>
  );
};

export default ChatInput;
