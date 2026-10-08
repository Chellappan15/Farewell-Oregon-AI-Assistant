import React from "react";
import {
  Menu,
  RotateCcw,
  Cpu,
  Radio,
  Loader2,
} from "lucide-react";
import IconButton from "../common/IconButton";
import Badge from "../common/Badge";

export interface HeaderProps {
  onToggleSidebar?: () => void;
  onToggleIntelligence?: () => void;
  isIntelligenceOpen?: boolean;
  onClearChat?: () => void;
  isMessagesLoading?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  onToggleIntelligence,
  isIntelligenceOpen = true,
  onClearChat,
  isMessagesLoading = false,
}) => {
  return (
    <header className="app-header">
      <div className="header-left">
        {onToggleSidebar && (
          <IconButton
            icon={<Menu size={20} />}
            label="Toggle Sidebar"
            onClick={onToggleSidebar}
            className="mobile-sidebar-toggle"
          />
        )}

        <div className="header-branding">
          <div className="header-title-wrapper">
            <h1 className="header-title">Days Gone Assistant</h1>
            <Badge variant="success" size="sm" dot className="header-status-badge">
              AI Online
            </Badge>
          </div>
          <p className="header-subtitle">Survival intelligence for Days Gone</p>
        </div>
      </div>

      <div className="header-actions">
        {isMessagesLoading ? (
          <div className="header-loading-tag">
            <Loader2 size={14} className="header-loading-spinner" />
            <span className="indicator-text">Loading Intel...</span>
          </div>
        ) : (
          <div className="header-indicator">
            <Radio size={14} className="radio-pulse" />
            <span className="indicator-text">Oregon Radio Link Active</span>
          </div>
        )}

        {!isMessagesLoading && onClearChat && (
          <IconButton
            icon={<RotateCcw size={16} />}
            label="Clear current conversation"
            variant="ghost"
            size="md"
            onClick={onClearChat}
          />
        )}

        {onToggleIntelligence && (
          <IconButton
            icon={<Cpu size={18} />}
            label="Toggle AI Intelligence Panel"
            variant={isIntelligenceOpen ? "primary" : "ghost"}
            size="md"
            active={isIntelligenceOpen}
            onClick={onToggleIntelligence}
          />
        )}
      </div>
    </header>
  );
};

export default Header;