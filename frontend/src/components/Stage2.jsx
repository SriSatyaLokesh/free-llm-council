import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import ToolTrace from './ToolTrace';
import { shortModel, formatTokens } from '../format';
import { Target, AlertTriangle } from './icons';
import './Stage2.css';
import './DebateMode.css';

/**
 * Stage 2: the open debate.
 *
 * Members see each other by real name here, so the layout is a round selector
 * plus a per-model column - it should read like a transcript, not a set of
 * disconnected answers.
 */
export default function Stage2({ debate, earlyConclusion, injectedGuidance = [] }) {
  const [roundIndex, setRoundIndex] = useState(0);

  if (!debate || debate.length === 0) {
    return null;
  }

  const safeIndex = Math.min(roundIndex, debate.length - 1);
  const current = debate[safeIndex];
  const statements = current?.statements || [];

  if (statements.length === 0) {
    return (
      <div className="stage stage2">
        <h3 className="stage-title">Stage 2: Debate</h3>
        <p className="stage-hint">No debate rounds were run.</p>
      </div>
    );
  }

  return (
    <div className="stage stage2">
      <h3 className="stage-title">Stage 2: Debate</h3>
      <p className="stage-hint">
        Members respond to each other by name - rebutting peers, conceding points,
        and saying whether they updated or held their position.
      </p>

      {injectedGuidance && injectedGuidance.length > 0 && (
        <div className="human-guidance-card">
          <div className="human-guidance-badge">
            <Target size={12} style={{ verticalAlign: 'middle', marginRight: 4 }} />
            Human Guidance Injected
          </div>
          {injectedGuidance.map((g, idx) => (
            <div key={idx} className="human-guidance-item">
              <div className="human-guidance-msg">"{g.message}"</div>
              {g.resources && g.resources.length > 0 && (
                <div className="human-guidance-resources">
                  <span className="resources-label">Resources: </span>
                  {g.resources.map((r, i) => (
                    <a
                      key={i}
                      href={r}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="guidance-link"
                    >
                      {r}
                    </a>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {earlyConclusion && (
        <div className="debate-early-banner">
          <AlertTriangle size={13} style={{ verticalAlign: 'middle', marginRight: 5 }} />
          Debate concluded early: {typeof earlyConclusion === 'object' ? `${earlyConclusion.reason || 'budget reached'}` : earlyConclusion}. Handed off cleanly to review and verdict.
        </div>
      )}

      {debate.length > 1 && (
        <div className="round-selector">
          {debate.map((round, index) => (
            <button
              key={round.round}
              className={`round-tab ${safeIndex === index ? 'active' : ''}`}
              onClick={() => setRoundIndex(index)}
            >
              Round {round.round}
              {round.cavemanLevel && round.cavemanLevel !== 'off' && (
                <span className="round-mode-badge">{round.cavemanLevel}</span>
              )}
            </button>
          ))}
        </div>
      )}

      {current?.compressed && (
        <p className="stage-hint">
          This round ran in <strong>{current.cavemanLevel}</strong> compression via
          the official Caveman skill: members argued in shorthand and did no new
          web research. The chairman expands it back into full prose.
        </p>
      )}

      {current?.tokens?.total > 0 && (
        <div className="stage-tokens">
          Round {current.round} used{' '}
          <strong>{current.tokens.total.toLocaleString()}</strong> tokens
          {current.tokens.output > 0 && ` (${current.tokens.output.toLocaleString()} written)`}
        </div>
      )}

      <div className="debate-grid">
        {statements.map((statement) => (
          <div key={statement.model} className="debate-card">
            <div className="stage-entry-header">
              <span className="model-name">{shortModel(statement.model)}</span>
              {formatTokens(statement.tokens) && (
                <span className="stage-entry-meta">
                  {formatTokens(statement.tokens)}
                </span>
              )}
            </div>

            {statement.error ? (
              <div className="stage-error">{statement.error}</div>
            ) : (
              <div className="debate-text markdown-content">
                <ReactMarkdown>{statement.response}</ReactMarkdown>
              </div>
            )}

            <ToolTrace toolCalls={statement.toolCalls} />
          </div>
        ))}
      </div>
    </div>
  );
}
