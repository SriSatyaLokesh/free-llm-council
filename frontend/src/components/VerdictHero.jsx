import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import ToolTrace from './ToolTrace';
import { shortModel, formatTokens } from '../format';
import { api } from '../api';
import { Zap, Target, FileText, Package } from './icons';
import './VerdictHero.css';

/**
 * The verdict is the product. This is the hero of the page: the chairman's
 * decision, its reasoning, the tradeoffs, the dissent, and how sure he is.
 *
 * Previously this was one tab among four. It is now the thing you see first.
 */

const SECTIONS = [
  { key: 'decision', label: 'Decision' },
  { key: 'reasoning', label: 'Reasoning' },
  { key: 'tradeoffs', label: 'Tradeoffs' },
  { key: 'dissent', label: 'Dissent' },
  { key: 'confidence', label: 'Confidence' },
];

export default function VerdictHero({
  verdict,
  compression,
  metadata,
  conversationId,
  onOpenReport,
}) {
  const [showRaw, setShowRaw] = useState(false);

  if (!verdict) return null;

  if (!verdict.response) {
    return (
      <section className="verdict-hero verdict-hero--empty">
        <h2 className="verdict-hero-title">Verdict</h2>
        {verdict.error ? (
          <p className="verdict-hero-error">{verdict.error}</p>
        ) : (
          <p className="verdict-hero-pending">The chairman is weighing the transcript.</p>
        )}
      </section>
    );
  }

  const sections = verdict.sections || {};
  const parsed = SECTIONS.filter(({ key }) => sections[key]);
  const total = compression?.total || 0;

  return (
    <section className="verdict-hero" aria-labelledby="verdict-heading">
      <header className="verdict-hero-head">
        <h2 className="verdict-hero-title" id="verdict-heading">
          The verdict
        </h2>
        <div className="verdict-hero-meta">
          {verdict.model && verdict.model !== 'error' && (
            <span className="verdict-chair">
              Chaired by {shortModel(verdict.model)}
              {metadata?.chairman_failover && (
                <span className="verdict-failover-badge" title="Intelligent Chairman Failover occurred">
                  <Zap size={11} style={{ verticalAlign: 'middle', marginRight: 3 }} />
                  Failover
                </span>
              )}
              {metadata?.injected_guidance && metadata.injected_guidance.length > 0 && (
                <span className="verdict-guidance-badge" title="Deliberation steered by human operator directives">
                  <Target size={11} style={{ verticalAlign: 'middle', marginRight: 3 }} />
                  Human Steered
                </span>
              )}
            </span>
          )}
          {formatTokens(verdict.tokens) && (
            <span className="verdict-tokens">{formatTokens(verdict.tokens)}</span>
          )}
        </div>
      </header>

      {parsed.length > 0 ? (
        <div className="verdict-sections">
          {parsed.map(({ key, label }) => (
            <div key={key} className={`verdict-section verdict-section--${key}`}>
              <h3 className="verdict-section-label">{label}</h3>
              <div className="verdict-body markdown-content">
                <ReactMarkdown>{sections[key]}</ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <>
          <p className="verdict-hero-pending">
            The chairman did not use the expected headings, so this is shown unparsed.
          </p>
          <div className="verdict-body markdown-content">
            <ReactMarkdown>{verdict.response}</ReactMarkdown>
          </div>
        </>
      )}

      <footer className="verdict-hero-foot">
        {total > 0 && (
          <span className="verdict-total">
            {total.toLocaleString()} tokens across the whole run
          </span>
        )}
        <div className="verdict-foot-actions">
          {conversationId && (
            <>
              <button
                type="button"
                className="verdict-export-btn verdict-report-btn"
                onClick={() => {
                  if (onOpenReport) {
                    onOpenReport();
                  } else {
                    window.open(api.getReportExportUrl(conversationId), '_blank');
                  }
                }}
                title="Open interactive deliberation report (Executive Brief & Deep-Dive Matrix)"
              >
                <FileText size={12} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                Deliberation Report
              </button>
              <button
                type="button"
                className="verdict-export-btn"
                onClick={() => window.open(api.getZipExportUrl(conversationId), '_blank')}
                title="Download full council debate package as ZIP"
              >
                <Package size={12} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                Export ZIP
              </button>
            </>
          )}
          <button
            type="button"
            className="verdict-raw-toggle"
            onClick={() => setShowRaw((v) => !v)}
            aria-expanded={showRaw}
          >
            {showRaw ? 'Hide raw response' : 'Show raw response'}
          </button>
        </div>
      </footer>

      {showRaw && (
        <div className="verdict-raw markdown-content">
          <ReactMarkdown>{verdict.response}</ReactMarkdown>
        </div>
      )}

      <ToolTrace toolCalls={verdict.toolCalls} />
    </section>
  );
}
