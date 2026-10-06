import { useState, useEffect } from 'react';
import { api } from '../api';
import './DebateMode.css';

const LEVEL_LABELS = {
  off: 'Off',
  lite: 'Lite',
  full: 'Full',
  ultra: 'Ultra',
  max: 'Max',
};

/**
 * Compression level for the model-to-model exchange.
 *
 * The level lives on the server, not in React state, so flipping it while a
 * run is in progress applies from the next debate round rather than the next
 * run. The rules themselves are the official Caveman skill, loaded by the
 * backend - this component only chooses a level.
 */
export default function DebateMode({ level, onChange, disabled }) {
  const [caveman, setCaveman] = useState(null);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    let cancelled = false;
    api
      .getSettings()
      .then((data) => !cancelled && setCaveman(data.caveman))
      .catch((err) => !cancelled && setError(err.message));
    return () => {
      cancelled = true;
    };
  }, []);

  const levels = caveman?.levels || ['off', 'lite', 'full', 'ultra', 'max'];
  const installed = caveman?.installed;
  const isCompressed = level && level !== 'off';

  const pick = async (next) => {
    setSaving(true);
    setError(null);
    try {
      await api.updateSettings({ debateMode: next });
      onChange(next);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="debate-mode">
      <div className="debate-mode-head">
        <span className="debate-mode-label">Debate compression</span>
        <span className="debate-mode-scope">debate rounds + blind review</span>
      </div>

      <div className="mode-buttons" role="group" aria-label="Debate compression level">
        {levels.map((option) => (
          <button
            key={option}
            type="button"
            className={`mode-button ${level === option ? 'active' : ''}`}
            onClick={() => pick(option)}
            disabled={disabled || saving || !installed}
            title={
              installed
                ? caveman.levelDescriptions[option] || 'No compression'
                : 'Caveman skill is not installed'
            }
          >
            {LEVEL_LABELS[option] || option}
          </button>
        ))}
      </div>

      {installed === false && (
        <div className="mode-note">
          Official Caveman skill not installed, so levels are unavailable.
          <code>{caveman?.installCommand}</code>
        </div>
      )}

      {installed && (
        <div className="mode-details">
          {caveman?.levelDescriptions?.[level] && (
            <div className="mode-description">
              <strong>{LEVEL_LABELS[level] || level}:</strong> {caveman.levelDescriptions[level]}
            </div>
          )}
          <p className="mode-note">
            {isCompressed ? (
              <>
                Agents deliberate in <strong>{level}</strong> shorthand to save tokens and latency. The chairman&rsquo;s final verdict is always synthesized in complete, professional prose for human reading.
              </>
            ) : (
              <>
                Members write normally without compression. Full-length human prose across all stages.
              </>
            )}
          </p>
        </div>
      )}

      {error && <div className="mode-error">{error}</div>}
    </div>
  );
}
