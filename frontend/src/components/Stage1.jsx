import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import ToolTrace from './ToolTrace';
import { shortModel, formatTokens } from '../format';
import './Stage1.css';

/**
 * Stage 1: every member's independent opening position.
 */
export default function Stage1({ responses }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!responses || responses.length === 0) {
    return null;
  }

  // Focus on active members who reported; non-reporting members are stated once on top of ProcessPanel
  const activeResponses = responses.filter(
    (r) => !r.error && (r.response || (r.toolCalls && r.toolCalls.length > 0))
  );
  const displayList = activeResponses.length > 0 ? activeResponses : responses;
  const active = displayList[Math.min(activeTab, displayList.length - 1)];

  return (
    <div className="stage stage1">
      <h3 className="stage-title">Stage 1: Opening Positions</h3>
      <p className="stage-hint">
        Each member answered independently, with web and workspace research available.
      </p>

      <div className="tabs">
        {displayList.map((resp, index) => (
          <button
            key={resp.model}
            className={`tab ${activeTab === index ? 'active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            {shortModel(resp.model)}
          </button>
        ))}
      </div>

      {active && (
        <div className="tab-content">
          <div className="stage-entry-header">
            <span className="model-name">{active.model}</span>
            {formatTokens(active.tokens) && (
              <span className="stage-entry-meta">{formatTokens(active.tokens)}</span>
            )}
          </div>

          {active.error ? (
            <div className="stage-error">{active.error}</div>
          ) : (
            <div className="response-text markdown-content">
              <ReactMarkdown>{active.response}</ReactMarkdown>
            </div>
          )}

          <ToolTrace toolCalls={active.toolCalls} />
        </div>
      )}
    </div>
  );
}
