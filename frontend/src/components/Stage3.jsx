import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { shortModel } from '../format';
import './Stage3.css';

/**
 * Stage 3: blind peer scoring.
 *
 * Positions are shown as Response A/B/C because that is what the reviewers saw.
 * The de-anonymised names are shown alongside so the raw text can be validated -
 * a reviewer may have reasoned about a different model than they thought.
 */
export default function Stage3({ reviews, labelToModel, aggregateRankings }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!reviews || reviews.length === 0) {
    return null;
  }

  const mapping = labelToModel || {};
  const aggregate = aggregateRankings || [];
  const safeIndex = Math.min(activeTab, reviews.length - 1);
  const active = reviews[safeIndex];

  return (
    <div className="stage stage3">
      <h3 className="stage-title">Stage 3: Blind Peer Review</h3>
      <p className="stage-hint">
        Positions were re-labelled so reviewers could not favour a known model.
        Bold names below are for your readability only - the reviewers saw labels.
      </p>

      {aggregate.length > 0 && (
        <div className="aggregate-block">
          <div className="aggregate-title">Aggregate ranking (lower is better)</div>
          <table className="aggregate-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Model</th>
                <th>Avg rank</th>
                <th>Reviews</th>
              </tr>
            </thead>
            <tbody>
              {aggregate.map((row, index) => (
                <tr key={row.model}>
                  <td>{index + 1}</td>
                  <td className="aggregate-model">{row.model}</td>
                  <td className="aggregate-rank">{row.average_rank}</td>
                  <td>{row.rankings_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="tabs">
        {reviews.map((review, index) => (
          <button
            key={review.model}
            className={`tab ${safeIndex === index ? 'active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            {shortModel(review.model)}
          </button>
        ))}
      </div>

      {active && (
        <div className="tab-content">
          <div className="model-name">{active.model}</div>

          {active.error ? (
            <div className="stage-error">{active.error}</div>
          ) : (
            <div className="response-text markdown-content">
              <ReactMarkdown>{active.ranking}</ReactMarkdown>
            </div>
          )}

          {active.parsed_ranking && active.parsed_ranking.length > 0 && (
            <div className="parsed-ranking">
              <div className="parsed-ranking-title">Extracted ranking</div>
              <div className="parsed-ranking-chips">
                {active.parsed_ranking.map((label, index) => (
                  <span key={`${label}-${index}`} className="parsed-chip">
                    <span className="parsed-chip-rank">{index + 1}</span>
                    <strong>{mapping[label] || label}</strong>
                    <span className="parsed-chip-label">{label}</span>
                  </span>
                ))}
              </div>
            </div>
          )}

          {active.parsed_ranking && active.parsed_ranking.length === 0 && (
            <div className="stage-warning">
              This reviewer did not produce a parseable ranking, so it does not
              count toward the aggregate above.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
