import { useEffect, useState } from 'react';
import { api } from '../api';
import DebateMode from './DebateMode';
import { Chevron, Check } from './icons';
import { shortModel } from '../format';
import { saveCouncilPreset, loadCouncilPreset, reconcilePreset } from '../presets';
import './ModelRoster.css';

/**
 * Helper to determine default reasoning level: Chairman defaults to max, members to medium or high.
 */
export function getDefaultThinking(model, isChairman) {
  if (!model || !model.variants || model.variants.length === 0) return '';
  const variantIds = model.variants.map((v) => (typeof v === 'string' ? v : v.id));
  if (isChairman) {
    if (variantIds.includes('max')) return 'max';
    if (variantIds.includes('xhigh')) return 'xhigh';
    if (variantIds.includes('high')) return 'high';
    return variantIds[variantIds.length - 1];
  }
  if (variantIds.includes('medium')) return 'medium';
  if (variantIds.includes('high')) return 'high';
  return variantIds[0];
}

/**
 * Council composition panel.
 *
 * The roster comes from opencode at runtime, so this always reflects the
 * models that are actually available - there is no hardcoded list.
 */
export default function ModelRoster({
  config,
  onChange,
  disabled,
  evictedModels = [],
  retiredModels = [],
  isSidebar = false,
}) {
  const [models, setModels] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [savedToast, setSavedToast] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const fetchRoster = () => {
      api
        .getModels()
        .then((data) => {
          if (cancelled) return;
          const fetchedModels = data.models || [];
          setModels(fetchedModels);

          if (fetchedModels.length > 0) {
            // Check if user has a persisted preset from a previous session
            const savedPreset = loadCouncilPreset();
            if (savedPreset) {
              const reconciled = reconcilePreset(savedPreset, fetchedModels, data.defaultChairman);
              if (reconciled && reconciled.members?.length > 0) {
                onChange(reconciled);
                return;
              }
            }

            const updates = {};
            if (data.defaultRounds != null && config.rounds == null) {
              updates.rounds = data.defaultRounds;
            }
            // Seat everyone by default, the first time we see the roster.
            if (!config.members || config.members.length === 0) {
              updates.members = fetchedModels.map((m) => m.id);
            }
            // Mirror the backend's chairman choice so the panel reflects it.
            const effectiveChairman = config.chairman || data.defaultChairman || (fetchedModels[0] ? fetchedModels[0].id : null);
            if (!config.chairman) {
              updates.chairman = effectiveChairman;
            }
            // Initialize default thinking configurations
            if (!config.modelThinking) {
              const initThinking = {};
              for (const m of fetchedModels) {
                if (m.variants && m.variants.length > 0) {
                  initThinking[m.id] = getDefaultThinking(m, m.id === effectiveChairman);
                }
              }
              updates.modelThinking = initThinking;
            }
            if (Object.keys(updates).length > 0) {
              onChange(updates);
            }
          }
        })
        .catch((err) => !cancelled && setError(err.message))
        .finally(() => !cancelled && setLoading(false));
    };

    fetchRoster();

    // Auto-retry polling every 4s if models list is still empty
    const interval = setInterval(() => {
      if (models.length === 0) {
        fetchRoster();
      }
    }, 4000);

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [models.length]);

  const members = config.members || [];
  const selected = models.filter((m) => members.includes(m.id));
  const dropped = members.filter((id) => !models.some((m) => m.id === id));

  const evictedMap = {};
  for (const ev of evictedModels) {
    if (ev?.model) evictedMap[ev.model] = ev;
  }
  const retiredMap = {};
  for (const ret of retiredModels) {
    if (ret?.model) retiredMap[ret.model] = ret;
  }

  const toggle = (id) => {
    const next = members.includes(id)
      ? members.filter((m) => m !== id)
      : [...members, id];
    onChange({ members: next });
  };

  const handleChairmanChange = (newChairmanId) => {
    const nextThinking = { ...(config.modelThinking || {}) };
    if (newChairmanId) {
      const chairModel = models.find((m) => m.id === newChairmanId);
      if (chairModel && chairModel.variants?.length) {
        nextThinking[newChairmanId] = getDefaultThinking(chairModel, true);
      }
    }
    onChange({ chairman: newChairmanId || null, modelThinking: nextThinking });
  };

  const handleThinkingChange = (modelId, variant) => {
    onChange({
      modelThinking: {
        ...(config.modelThinking || {}),
        [modelId]: variant,
      },
    });
  };

  const handleSaveDefault = () => {
    const ok = saveCouncilPreset(config);
    if (ok) {
      setSavedToast(true);
      setTimeout(() => setSavedToast(false), 2200);
    }
  };

  if (loading) {
    return <div className="roster-summary">Asking opencode which models are available...</div>;
  }

  if (error) {
    return (
      <div className="roster-summary roster-error">
        <strong>Cannot reach opencode.</strong> {error}
      </div>
    );
  }

  const renderPanelContent = () => (
    <>
      <div className="roster-section roster-controls">
        <label className="roster-field">
          <span className="roster-field-label">Chairman</span>
          <select
            value={config.chairman || ''}
            onChange={(e) => handleChairmanChange(e.target.value)}
            disabled={disabled}
          >
            <option value="">Auto (highest intelligence)</option>
            {models.map((model) => (
              <option key={model.id} value={model.id}>
                {shortModel(model.id)} {model.context ? `(${Math.round(model.context / 1000)}k ctx)` : ''}
              </option>
            ))}
          </select>
        </label>

        <label className="roster-field">
          <span className="roster-field-label">Debate rounds</span>
          <div className="rounds-control">
            <button
              type="button"
              onClick={() => onChange({ rounds: Math.max(0, (config.rounds ?? 2) - 1) })}
              disabled={disabled || (config.rounds ?? 2) <= 0}
            >
              −
            </button>
            <span className="rounds-value">{config.rounds ?? 2}</span>
            <button
              type="button"
              onClick={() => onChange({ rounds: Math.min(5, (config.rounds ?? 2) + 1) })}
              disabled={disabled || (config.rounds ?? 2) >= 5}
            >
              +
            </button>
          </div>
        </label>
      </div>

      <div className="roster-section">
        <div className="roster-section-header-row">
          <div className="roster-section-title">Members & Thinking Quality</div>
          <div className="roster-bulk-actions">
            <button
              type="button"
              className="roster-bulk-btn"
              onClick={() => onChange({ members: models.map((m) => m.id) })}
              disabled={disabled}
              title="Seat all available models"
            >
              All
            </button>
            <button
              type="button"
              className="roster-bulk-btn"
              onClick={() => onChange({ members: [] })}
              disabled={disabled}
              title="Clear all seated models"
            >
              None
            </button>
          </div>
        </div>
        <div className="roster-models">
              {models.map((model) => {
                const isChair = model.id === config.chairman;
                const currentThinking =
                  config.modelThinking?.[model.id] || getDefaultThinking(model, isChair);
                return (
                  <div key={model.id} className="roster-model-row">
                    <label className="roster-model">
                      <input
                        type="checkbox"
                        checked={members.includes(model.id)}
                        onChange={() => toggle(model.id)}
                        disabled={disabled}
                      />
                      <span className="roster-model-body">
                        <span className="roster-model-name">
                          {shortModel(model.id)}
                          {isChair && (
                            <span
                              className="model-status-badge badge-chairman"
                              title="Designated Chairman / Main Decider"
                            >
                              Chairman
                            </span>
                          )}
                          {evictedMap[model.id] && (
                            <span
                              className="model-status-badge badge-evicted"
                              title={`Evicted: ${evictedMap[model.id].reason || 'Model failed'}`}
                            >
                              Evicted
                            </span>
                          )}
                          {retiredMap[model.id] && (
                            <span
                              className="model-status-badge badge-retired"
                              title={`Retired: ${retiredMap[model.id].reason || 'Token cap reached'}`}
                            >
                              Cap Reached
                            </span>
                          )}
                        </span>
                        <span className="roster-model-meta">
                          {model.context ? `${Math.round(model.context / 1000)}k ctx` : ''}
                          {model.supportsTools ? ' · tools' : ''}
                          {model.free ? ' · free' : ''}
                        </span>
                      </span>
                    </label>

                    <div className="roster-model-thinking">
                      {model.variants && model.variants.length > 0 ? (
                        <select
                          className="thinking-select"
                          value={currentThinking}
                          onChange={(e) => handleThinkingChange(model.id, e.target.value)}
                          disabled={disabled || !members.includes(model.id)}
                          title={`Reasoning effort for ${shortModel(model.id)}`}
                        >
                          {model.variants.map((v) => {
                            const vId = typeof v === 'string' ? v : v.id;
                            return (
                              <option key={vId} value={vId}>
                                {vId} thinking
                              </option>
                            );
                          })}
                        </select>
                      ) : (
                        <span className="thinking-none" title="Standard reasoning (no variants)">
                          standard
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
            {dropped.length > 0 && (
              <div className="stage-warning">
                No longer available in opencode: {dropped.join(', ')}
              </div>
            )}
            {members.length < 2 && (
              <div className="stage-warning">
                A council needs at least 2 members to debate.
              </div>
            )}
          </div>

      <div className="roster-section roster-budgets">
        <div className="roster-section-title">Token & Time Limits</div>
        <div className="budget-grid">
          <label className="roster-field">
            <span className="roster-field-label">Per-Model Token Cap</span>
            <select
              value={config.tokenCapPerModel ?? ''}
              onChange={(e) =>
                onChange({
                  tokenCapPerModel: e.target.value ? Number(e.target.value) : null,
                })
              }
              disabled={disabled}
            >
              <option value="">No limit</option>
              <option value="5000">5,000 tokens</option>
              <option value="10000">10,000 tokens</option>
              <option value="25000">25,000 tokens</option>
              <option value="50000">50,000 tokens</option>
            </select>
          </label>

          <label className="roster-field">
            <span className="roster-field-label">Global Token Budget</span>
            <select
              value={config.tokenBudgetTotal ?? ''}
              onChange={(e) =>
                onChange({
                  tokenBudgetTotal: e.target.value ? Number(e.target.value) : null,
                })
              }
              disabled={disabled}
            >
              <option value="">No limit</option>
              <option value="20000">20,000 tokens</option>
              <option value="50000">50,000 tokens</option>
              <option value="100000">100,000 tokens</option>
              <option value="250000">250,000 tokens</option>
            </select>
          </label>

          <label className="roster-field">
            <span className="roster-field-label">Time Limit</span>
            <select
              value={config.timeLimitSeconds ?? ''}
              onChange={(e) =>
                onChange({
                  timeLimitSeconds: e.target.value ? Number(e.target.value) : null,
                })
              }
              disabled={disabled}
            >
              <option value="">No limit</option>
              <option value="60">60 seconds</option>
              <option value="120">2 minutes</option>
              <option value="300">5 minutes</option>
              <option value="600">10 minutes</option>
            </select>
          </label>
        </div>
      </div>

      <div className="roster-section roster-preset-section">
        <button
          type="button"
          className={`btn-persist-settings ${savedToast ? 'saved' : ''}`}
          onClick={handleSaveDefault}
          disabled={disabled}
          title="Save current model roster, thinking qualities, rounds, debate compression, and budget caps as default for future debates"
        >
          {savedToast ? (
            <>
              <Check size={12} style={{ verticalAlign: 'middle', marginRight: 4 }} />
              Settings Persisted as Default
            </>
          ) : (
            'Save as Default Preset'
          )}
        </button>
        <span className="preset-note">
          {savedToast
            ? 'Persisted! This setup will load automatically for future debates.'
            : 'Saves your current council roster, thinking levels, and limits.'}
        </span>
      </div>

      <div className="roster-footnote">
        {selected.length > 0 && config.rounds > 0 ? (
          <>
            This run will make roughly{' '}
            <strong>
              {selected.length * (2 + (config.rounds ?? 2)) + 1}
            </strong>{' '}
            model calls, and can take several minutes because members research
            with live web tools.
          </>
        ) : (
          'Set the debate rounds to 0 to run a single pass with no debate.'
        )}
      </div>

      <DebateMode
        level={config.debateMode}
        onChange={(debateMode) => onChange({ debateMode })}
        disabled={disabled}
      />
    </>
  );

  if (isSidebar) {
    return (
      <div className="roster-panel roster-sidebar-panel">
        {renderPanelContent()}
      </div>
    );
  }

  return (
    <div className={`roster ${open ? 'open' : ''}`}>
      <button
        type="button"
        className="roster-summary"
        onClick={() => setOpen((v) => !v)}
        disabled={disabled}
      >
        <span className="roster-count">
          {selected.length} / {models.length} members
        </span>
        <span className="roster-detail">
          {selected.length > 0
            ? selected
                .map((m) => {
                  const isChair = m.id === config.chairman;
                  const th = config.modelThinking?.[m.id] || getDefaultThinking(m, isChair);
                  return th ? `${shortModel(m.id)} (${th})` : shortModel(m.id);
                })
                .join(', ')
            : 'select the council'}
        </span>
        <span className="roster-chevron" aria-hidden="true">
          <Chevron open={open} size={14} />
        </span>
      </button>

      {open && <div className="roster-panel">{renderPanelContent()}</div>}
    </div>
  );
}
