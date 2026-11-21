import React, { useState, useRef, useEffect } from "react";
import { Send, CornerDownLeft, Layers, ChevronUp, Check, Gamepad2 } from "lucide-react";
import { useChat } from "../../context/ChatContext";
import type { GameKey, RetrievalMode } from "../../types/chat";
import { GAME_OPTIONS, getGameProfile } from "../../utils/games";

const RETRIEVAL_OPTIONS: { value: RetrievalMode; label: string; description: string }[] = [
  { value: "hybrid", label: "Hybrid", description: "Vector + BM25, fused and reranked" },
  { value: "dense", label: "Dense", description: "Vector (semantic) search only" },
  { value: "text", label: "Text", description: "BM25 keyword search only" },
];

const GAME_MENU_OPTIONS: { value: GameKey; label: string; description: string }[] = GAME_OPTIONS.map(
  (profile) => ({ value: profile.key, label: profile.label, description: profile.description })
);

interface OptionMenuProps<T extends string> {
  icon: React.ReactNode;
  title: string;
  value: T;
  options: { value: T; label: string; description: string }[];
  onChange: (value: T) => void;
  disabled?: boolean;
}

// Small dropdown used for both the game and the retrieval pickers
function OptionMenu<T extends string>({ icon, title, value, options, onChange, disabled }: OptionMenuProps<T>) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close the menu when clicking outside it
  useEffect(() => {
    if (!isOpen) return;
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen]);

  const active = options.find((option) => option.value === value) ?? options[0];

  return (
    <div className="retrieval-mode" ref={menuRef}>
      <button
        type="button"
        onClick={() => setIsOpen((open) => !open)}
        disabled={disabled}
        className="retrieval-mode-button"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        title={`${title}: ${active.label}`}
      >
        {icon}
        <span>{active.label}</span>
        <ChevronUp size={12} />
      </button>

      {isOpen && (
        <ul className="retrieval-mode-menu" role="listbox" aria-label={title}>
          {options.map((option) => (
            <li key={option.value}>
              <button
                type="button"
                role="option"
                aria-selected={option.value === value}
                className={`retrieval-mode-option ${option.value === value ? "active" : ""}`}
                onClick={() => {
                  onChange(option.value);
                  setIsOpen(false);
                }}
              >
                <span className="retrieval-mode-option-text">
                  <span className="retrieval-mode-option-label">{option.label}</span>
                  <span className="retrieval-mode-option-desc">{option.description}</span>
                </span>
                {option.value === value && <Check size={14} />}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

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
  const { retrievalMode, setRetrievalMode, game, setGame } = useChat();
  const profile = getGameProfile(game);

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
        <OptionMenu
          icon={<Gamepad2 size={14} />}
          title="Game"
          value={game}
          options={GAME_MENU_OPTIONS}
          onChange={setGame}
          disabled={disabled}
        />

        <OptionMenu
          icon={<Layers size={14} />}
          title="Retrieval"
          value={retrievalMode}
          options={RETRIEVAL_OPTIONS}
          onChange={setRetrievalMode}
          disabled={disabled}
        />

        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={profile.placeholder}
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
          {profile.assistantName} can use game knowledge, conversation memory and tools.
        </span>
        <span className="chat-input-shortcut">
          <CornerDownLeft size={11} /> Enter to send • Shift+Enter for newline
        </span>
      </div>
    </div>
  );
};

export default ChatInput;
