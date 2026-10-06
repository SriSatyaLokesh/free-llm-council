import { useState } from 'react';
import { toolCallLabel } from '../format';
import './ToolTrace.css';

/**
 * Shows which tools a model actually used - web fetches, searches, file reads.
 *
 * This is the audit trail for the council's claim that it did its research:
 * every chip is a real call recorded by opencode, and clicking one reveals the
 * output the model saw.
 */
export default function ToolTrace({ toolCalls }) {
  const [openIndex, setOpenIndex] = useState(null);

  if (!toolCalls || toolCalls.length === 0) {
    return null;
  }

  return (
    <div className="tool-trace">
      <div className="tool-trace-label">Tools used</div>
      <div className="tool-chips">
        {toolCalls.map((call, index) => {
          const isOpen = openIndex === index;
          const denied = call.status === 'denied' || call.status === 'error';
          return (
            <span key={index} className="tool-chip-wrapper">
              <button
                type="button"
                className={`tool-chip ${denied ? 'denied' : ''} ${isOpen ? 'open' : ''}`}
                onClick={() => setOpenIndex(isOpen ? null : index)}
                title={denied ? 'Blocked by the council sandbox' : 'Show what this tool returned'}
              >
                <span className="tool-chip-name">{call.name}</span>
                {toolCallLabel(call) !== call.name && (
                  <span className="tool-chip-detail">{toolCallLabel(call)}</span>
                )}
                {denied && <span className="tool-chip-badge">blocked</span>}
              </button>
              {isOpen && (
                <span className="tool-chip-output">
                  {call.url && <code className="tool-chip-url">{call.url}</code>}
                  <pre>{call.output || call.error || '(no output recorded)'}</pre>
                </span>
              )}
            </span>
          );
        })}
      </div>
    </div>
  );
}
