import { useEffect, useState } from 'react';
import { Check, Target } from './icons';
import { shortModel } from '../format';
import { api } from '../api';
import './RunRail.css';

/**
 * Live progress for a council run.
 *
 * This exists because the skill's UX rules flag "loading spinner for 10s+"
 * as an anti-pattern, and a council run takes minutes, not seconds. The rail
 * answers the three questions a bare spinner leaves open: which stage, which
 * model, and how long so far.
 *
 * `aria-live="polite"` announces stage changes without stealing focus.
 */

const STAGES = [
  { key: 'positions', label: 'Positions', n: 1 },
  { key: 'debate', label: 'Debate', n: 2 },
  { key: 'review', label: 'Review', n: 3 },
  { key: 'verdict', label: 'Verdict', n: 4 },
];

function useElapsed(active, startedAt) {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    if (!active) return undefined;
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, [active]);

  if (!startedAt) return 0;
  return Math.max(0, Math.floor((now - startedAt) / 1000));
}

function formatElapsed(seconds) {
  if (seconds < 60) return `${seconds}s`;
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}m ${String(s).padStart(2, '0')}s`;
}

export default function RunRail({
  council,
  loading,
  members,
  chairman,
  startedAt,
  conversationId,
}) {
  const active = Boolean(loading && Object.values(loading).some(Boolean));
  const elapsed = useElapsed(active, startedAt);

  const [steerOpen, setSteerOpen] = useState(false);
  const [steerMessage, setSteerMessage] = useState('');
  const [steerResources, setSteerResources] = useState('');
  const [isSubmittingSteer, setIsSubmittingSteer] = useState(false);
  const [steerStatus, setSteerStatus] = useState(null);

  const debate = council?.debate || [];
  const positions = council?.positions || [];

  // Which stage is in flight right now.
  const done = {
    positions: positions.length > 0,
    debate: debate.length > 0,
    review: (council?.review || []).length > 0,
    verdict: Boolean(council?.verdict?.response),
  };
  const current = STAGES.find((s) => !done[s.key])?.key ?? 'verdict';

  // How far along the current stage we are, and who is working.
  let detail = '';
  if (current === 'positions') {
    detail = `${positions.length} of ${members?.length || '?'} members reported`;
  } else if (current === 'debate') {
    const rounds = debate.length;
    detail = rounds
      ? `${rounds} round${rounds === 1 ? '' : 's'} complete`
      : 'opening the debate';
  } else if (current === 'review') {
    detail = `${(council?.review || []).length} of ${members?.length || '?'} scored`;
  } else if (current === 'verdict') {
    detail = 'chairman is weighing the transcript';
  }

  const activeLevel = debate[debate.length - 1]?.cavemanLevel;

  const handleSteerSubmit = async (e) => {
    e.preventDefault();
    if (!steerMessage.trim() || !conversationId) return;

    setIsSubmittingSteer(true);
    setSteerStatus(null);
    try {
      const resList = steerResources
        .split(/[,\n]/)
        .map((r) => r.trim())
        .filter(Boolean);
      await api.steerDebate(conversationId, steerMessage.trim(), resList);
      setSteerStatus('success');
      setSteerMessage('');
      setSteerResources('');
      setTimeout(() => {
        setSteerStatus(null);
        setSteerOpen(false);
      }, 3000);
    } catch (err) {
      setSteerStatus(`error: ${err.message}`);
    } finally {
      setIsSubmittingSteer(false);
    }
  };

  return (
    <div className="run-rail-wrapper">
      <div className="run-rail" role="status" aria-live="polite">
        <ol className="run-steps">
          {STAGES.map((stage) => {
            const isDone = done[stage.key];
            const isCurrent = active && current === stage.key;
            const state = isDone ? 'done' : isCurrent ? 'active' : 'pending';
            return (
              <li key={stage.key} className={`run-step ${state}`}>
                <span className="run-step-dot" aria-hidden="true">
                  {isDone ? <Check size={12} /> : stage.n}
                </span>
                <span className="run-step-label">{stage.label}</span>
              </li>
            );
          })}
        </ol>

        <div className="run-rail-meta">
          {active ? (
            <>
              <span className="run-rail-detail">{detail}</span>
              <span className="run-rail-timer">{formatElapsed(elapsed)}</span>
              {conversationId && (
                <button
                  type="button"
                  className={`run-rail-steer-btn ${steerOpen ? 'active' : ''}`}
                  onClick={() => setSteerOpen((v) => !v)}
                  title="Inject human operator guidance or resources mid-debate"
                >
                  <Target size={12} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                  Steer Debate
                </button>
              )}
            </>
          ) : (
            <span className="run-rail-detail run-rail-idle">
              {chairman ? `Chaired by ${shortModel(chairman)}` : 'Council idle'}
            </span>
          )}
        </div>

        {activeLevel && activeLevel !== 'off' && (
          <span className="run-rail-level" title={`Debate compression: ${activeLevel}`}>
            {activeLevel}
          </span>
        )}

        {active && (
          <span className="run-rail-pulse" aria-hidden="true" />
        )}
      </div>

      {steerOpen && active && (
        <form className="run-rail-steer-form" onSubmit={handleSteerSubmit}>
          <div className="steer-form-header">
            <strong>
              <Target size={13} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              Human-in-the-Loop Steering & Resource Injection
            </strong>
            <span className="steer-form-sub">
              Direct the council's focus or supply new facts. Injected guidance takes effect in subsequent rounds and the final verdict.
            </span>
          </div>

          <div className="steer-form-body">
            <label className="steer-form-label">
              Directive / Guidance
              <textarea
                className="steer-textarea"
                rows={2}
                placeholder="e.g. Focus strictly on partition pruning. Disregard MongoDB completely."
                value={steerMessage}
                onChange={(e) => setSteerMessage(e.target.value)}
                required
              />
            </label>

            <label className="steer-form-label">
              Resource URLs / References (optional, comma-separated)
              <input
                type="text"
                className="steer-input"
                placeholder="https://postgresql.org/docs, https://clickhouse.com"
                value={steerResources}
                onChange={(e) => setSteerResources(e.target.value)}
              />
            </label>
          </div>

          <div className="steer-form-actions">
            {steerStatus === 'success' && (
              <span className="steer-success-msg">
                <Check size={12} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                Directive injected! Models will address in upcoming round.
              </span>
            )}
            {steerStatus && steerStatus.startsWith('error') && (
              <span className="steer-error-msg">{steerStatus}</span>
            )}

            <button
              type="button"
              className="steer-cancel-btn"
              onClick={() => setSteerOpen(false)}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="steer-submit-btn"
              disabled={isSubmittingSteer || !steerMessage.trim()}
            >
              {isSubmittingSteer ? 'Injecting…' : 'Inject Directive'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
