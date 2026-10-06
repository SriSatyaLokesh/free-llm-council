import { useState } from 'react';
import Stage1 from './Stage1';
import Stage2 from './Stage2';
import Stage3 from './Stage3';
import { Chevron } from './icons';
import './ProcessPanel.css';

/**
 * The council process, collapsed by default.
 *
 * The verdict leads the page; this is the evidence behind it. It stays one
 * click away rather than being deleted, because the original promise of this
 * project is that you can inspect exactly what every model said.
 */

const STAGES = [
  { key: 'positions', label: 'Opening positions', n: 1 },
  { key: 'debate', label: 'Debate', n: 2 },
  { key: 'review', label: 'Blind peer review', n: 3 },
];

export default function ProcessPanel({ council }) {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState('positions');

  const positions = council?.positions || [];
  const debate = council?.debate || [];
  const review = council?.review || [];

  const counts = {
    positions: positions.length,
    debate: debate.length,
    review: review.length,
  };

  // A member that failed must not vanish silently. Say so once, at the top of
  // the process, rather than as a silent omission in a tab.
  const failures = [
    ...positions,
    ...debate.flatMap((r) => r.statements || []),
    ...review,
  ].filter((entry) => entry?.error);
  const failedModels = [...new Set(failures.map((f) => f.model))];

  const total = counts.positions + counts.debate + counts.review;
  if (total === 0) return null;

  // Land on whichever stage has the most to show.
  const initial =
    counts.debate > 0 ? 'debate' : counts.positions > 0 ? 'positions' : 'review';

  const current = STAGES.find((s) => s.key === (open ? active : initial)) || STAGES[0];

  return (
    <section className="process" aria-labelledby="process-heading">
      <h2 className="sr-only" id="process-heading">
        Council process
      </h2>

      {failedModels.length > 0 && (
        <div className="process-failures" role="status">
          <strong>
            {failedModels.length} member{failedModels.length > 1 ? 's' : ''} did not
            return a complete answer
          </strong>
          : {failedModels.join(', ')}. They were left out of the tally; the
          remaining members carried the run.
        </div>
      )}

      <button
        type="button"
        className={`process-toggle ${open ? 'open' : ''}`}
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-controls="process-body"
      >
        <span className="process-toggle-caret" aria-hidden="true">
          <Chevron open={open} />
        </span>
        <span className="process-toggle-label">How the council got there</span>
        <span className="process-toggle-meta">
          {total} artefact{total === 1 ? '' : 's'}
        </span>
      </button>

      {open && (
        <div className="process-body" id="process-body">
          <div className="process-tabs" role="tablist" aria-label="Council stages">
            {STAGES.map((stage) => (
              <button
                key={stage.key}
                type="button"
                role="tab"
                id={`process-tab-${stage.key}`}
                aria-selected={current.key === stage.key}
                aria-controls={`process-panel-${stage.key}`}
                className={`process-tab ${current.key === stage.key ? 'active' : ''}`}
                onClick={() => setActive(stage.key)}
              >
                <span className="process-tab-n">{stage.n}</span>
                <span className="process-tab-label">{stage.label}</span>
                <span className="process-tab-count">{counts[stage.key]}</span>
              </button>
            ))}
          </div>

          <div
            className="process-stage"
            role="tabpanel"
            id={`process-panel-${current.key}`}
            aria-labelledby={`process-tab-${current.key}`}
          >
            {current.key === 'positions' && <Stage1 responses={positions} />}
            {current.key === 'debate' && (
              <Stage2
                debate={debate}
                injectedGuidance={council?.metadata?.injected_guidance}
                earlyConclusion={
                  council?.metadata?.early_conclusion ||
                  council?.metadata?.early_conclusion_reason
                }
              />
            )}
            {current.key === 'review' && (
              <Stage3
                reviews={review}
                labelToModel={council?.metadata?.label_to_model}
                aggregateRankings={
                  council?.metadata?.aggregate_rankings || council?.aggregate
                }
              />
            )}
          </div>
        </div>
      )}
    </section>
  );
}
