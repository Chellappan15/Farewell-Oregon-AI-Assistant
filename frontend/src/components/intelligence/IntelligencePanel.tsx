import React from "react";
import {
  Cpu,
  Database,
  Wrench,
  BrainCircuit,
  CheckCircle2,
  Layers,
  Sparkles,
  X,
} from "lucide-react";
import Badge from "../common/Badge";
import IconButton from "../common/IconButton";

export interface IntelligencePanelProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const IntelligencePanel: React.FC<IntelligencePanelProps> = ({
  isOpen = true,
  onClose,
}) => {
  if (!isOpen) return null;

  return (
    <aside className="intelligence-panel">
      {/* Header */}
      <div className="intelligence-header">
        <div className="intelligence-title-row">
          <div className="intelligence-icon-tag">
            <Cpu size={18} className="text-emerald" />
          </div>
          <div>
            <h3>AI Intelligence</h3>
            <span className="intelligence-caption">Architecture & Subsystems</span>
          </div>
        </div>

        <div className="intelligence-header-actions">
          <Badge variant="success" size="sm" dot>
            OPERATIONAL
          </Badge>
          {onClose && (
            <IconButton
              icon={<X size={16} />}
              label="Close Intelligence Panel"
              size="sm"
              onClick={onClose}
              className="intelligence-close-btn"
            />
          )}
        </div>
      </div>

      {/* Subsystem Cards */}
      <div className="intelligence-body">
        <div className="subsystems-group">
          <div className="group-label">
            <span>CORE SUBSYSTEMS</span>
          </div>

          {/* RAG Status */}
          <div className="subsystem-card">
            <div className="subsystem-card-top">
              <div className="subsystem-title-row">
                <Database size={16} className="subsystem-icon icon-blue" />
                <span className="subsystem-name">RAG Knowledge Retrieval</span>
              </div>
              <Badge variant="success" size="sm">Ready</Badge>
            </div>
            <p className="subsystem-desc">
              ChromaDB vector database indexed with Days Gone weapons, Freakers, and tactical survival lore.
            </p>
            <div className="subsystem-meta">
              <span className="meta-tag">1,240 Chunks Indexed</span>
              <span className="meta-tag">ChromaDB</span>
            </div>
          </div>

          {/* Conversation Memory Status */}
          <div className="subsystem-card">
            <div className="subsystem-card-top">
              <div className="subsystem-title-row">
                <Layers size={16} className="subsystem-icon icon-purple" />
                <span className="subsystem-name">Conversation Memory</span>
              </div>
              <Badge variant="success" size="sm">Ready</Badge>
            </div>
            <p className="subsystem-desc">
              Persistent multi-turn dialog tracking via MySQL store for context-aware tactical continuity.
            </p>
            <div className="subsystem-meta">
              <span className="meta-tag">MySQL Store</span>
              <span className="meta-tag">Active Context</span>
            </div>
          </div>

          {/* Tools Status */}
          <div className="subsystem-card">
            <div className="subsystem-card-top">
              <div className="subsystem-title-row">
                <Wrench size={16} className="subsystem-icon icon-amber" />
                <span className="subsystem-name">Tools Registry</span>
              </div>
              <Badge variant="success" size="sm">Ready</Badge>
            </div>
            <p className="subsystem-desc">
              Function calling enabled with specialized game telemetry tools.
            </p>
            <div className="subsystem-meta">
              <span className="meta-tag">compare_weapons</span>
              <span className="meta-tag">zombie_details</span>
            </div>
          </div>

          {/* Agent Loop Status */}
          <div className="subsystem-card">
            <div className="subsystem-card-top">
              <div className="subsystem-title-row">
                <BrainCircuit size={16} className="subsystem-icon icon-emerald" />
                <span className="subsystem-name">Agent & Tool Loop</span>
              </div>
              <Badge variant="success" size="sm">Ready</Badge>
            </div>
            <p className="subsystem-desc">
              Autonomous reasoning cycle capable of multi-step tool execution and response synthesis.
            </p>
            <div className="subsystem-meta">
              <span className="meta-tag">Gemini API</span>
              <span className="meta-tag">Loop Ready</span>
            </div>
          </div>
        </div>

        {/* AI Pipeline Architecture Schema */}
        <div className="pipeline-section">
          <div className="group-label">
            <span>PIPELINE FLOW</span>
          </div>

          <div className="pipeline-flow-card">
            <div className="pipeline-step">
              <div className="step-bullet">1</div>
              <div className="step-info">
                <strong>Survivor Query</strong>
                <span>User asks combat/strategy question</span>
              </div>
            </div>

            <div className="step-connector" />

            <div className="pipeline-step">
              <div className="step-bullet">2</div>
              <div className="step-info">
                <strong>Context & Vector Search</strong>
                <span>ChromaDB RAG + MySQL session history</span>
              </div>
            </div>

            <div className="step-connector" />

            <div className="pipeline-step">
              <div className="step-bullet">3</div>
              <div className="step-info">
                <strong>Gemini Reasoning & Tools</strong>
                <span>Autonomous tool execution loop</span>
              </div>
            </div>

            <div className="step-connector" />

            <div className="pipeline-step">
              <div className="step-bullet">4</div>
              <div className="step-info">
                <strong>Tactical Briefing</strong>
                <span>Markdown output delivered to survivor</span>
              </div>
            </div>
          </div>
        </div>

        {/* System Diagnostics / Telemetry */}
        <div className="telemetry-section">
          <div className="telemetry-grid">
            <div className="telemetry-item">
              <span className="telemetry-label">LLM Engine</span>
              <span className="telemetry-value">
                <Sparkles size={12} className="text-emerald" /> Google Gemini
              </span>
            </div>
            <div className="telemetry-item">
              <span className="telemetry-label">Game Profile</span>
              <span className="telemetry-value">Days Gone</span>
            </div>
            <div className="telemetry-item">
              <span className="telemetry-label">Health</span>
              <span className="telemetry-value text-emerald">
                <CheckCircle2 size={12} /> Optimal
              </span>
            </div>
            <div className="telemetry-item">
              <span className="telemetry-label">Target</span>
              <span className="telemetry-value">FastAPI</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default IntelligencePanel;