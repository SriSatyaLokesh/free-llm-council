import { useState, useEffect } from 'react';
import { api } from '../api';
import { XMark } from './icons';
import './ProviderKeyModal.css';

const PROVIDERS = [
  {
    id: 'openrouter',
    label: 'OpenRouter',
    placeholder: 'sk-or-v1-...',
    docs: 'https://openrouter.ai/keys',
    description: 'Access 200+ models including Claude 3.5 Sonnet, DeepSeek R1, Llama 3.3, and GPT-4o.',
  },
  {
    id: 'openai',
    label: 'OpenAI',
    placeholder: 'sk-proj-...',
    docs: 'https://platform.openai.com/api-keys',
    description: 'Direct access to GPT-4o, GPT-4o-mini, and o1 reasoning models.',
  },
  {
    id: 'anthropic',
    label: 'Anthropic',
    placeholder: 'sk-ant-api03-...',
    docs: 'https://console.anthropic.com/settings/keys',
    description: 'Direct access to Claude 3.5 Sonnet, Haiku, and Opus.',
  },
];

export default function ProviderKeyModal({ isOpen, onClose, onKeysUpdated }) {
  const [keysStatus, setKeysStatus] = useState({});
  const [inputs, setInputs] = useState({});
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    if (!isOpen) return;
    loadKeys();
  }, [isOpen]);

  const loadKeys = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await api.getProviderKeys();
      setKeysStatus(data || {});
    } catch (err) {
      setErrorMsg(err.message || 'Failed to load provider key status');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (providerId) => {
    const val = (inputs[providerId] || '').trim();
    if (!val) return;

    setErrorMsg(null);
    setStatusMsg(null);
    try {
      await api.updateProviderKey(providerId, val);
      setInputs((prev) => ({ ...prev, [providerId]: '' }));
      setStatusMsg(`Updated ${providerId} key successfully.`);
      await loadKeys();
      if (onKeysUpdated) onKeysUpdated();
    } catch (err) {
      setErrorMsg(err.message || `Failed to update ${providerId} key`);
    }
  };

  const handleRemove = async (providerId) => {
    setErrorMsg(null);
    setStatusMsg(null);
    try {
      await api.updateProviderKey(providerId, '');
      setStatusMsg(`Removed ${providerId} key.`);
      await loadKeys();
      if (onKeysUpdated) onKeysUpdated();
    } catch (err) {
      setErrorMsg(err.message || `Failed to remove ${providerId} key`);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <header className="modal-header">
          <div>
            <h2 id="modal-title">Provider API Keys</h2>
            <p className="modal-subtitle">
              Local OpenCode models are always 100% free and zero-config. Add optional API keys below to seat frontier cloud models alongside them.
            </p>
          </div>
          <button type="button" className="modal-close-btn" onClick={onClose} aria-label="Close dialog">
            <XMark size={14} />
          </button>
        </header>

        {statusMsg && <div className="modal-alert modal-alert-success">{statusMsg}</div>}
        {errorMsg && <div className="modal-alert modal-alert-error">{errorMsg}</div>}

        <div className="provider-list">
          {PROVIDERS.map((prov) => {
            const status = keysStatus[prov.id];
            const isConfigured = Boolean(status?.configured);
            const preview = status?.preview;

            return (
              <div key={prov.id} className="provider-card">
                <div className="provider-header">
                  <div className="provider-info">
                    <span className="provider-name">{prov.label}</span>
                    <span className={`provider-status ${isConfigured ? 'configured' : 'unconfigured'}`}>
                      {isConfigured ? `Configured (${preview})` : 'Not configured'}
                    </span>
                  </div>
                  {prov.docs && (
                    <a href={prov.docs} target="_blank" rel="noopener noreferrer" className="provider-docs-link">
                      Get Key ↗
                    </a>
                  )}
                </div>

                <p className="provider-desc">{prov.description}</p>

                <div className="provider-actions">
                  <input
                    type="password"
                    className="provider-input"
                    placeholder={isConfigured ? 'Paste new key to replace…' : prov.placeholder}
                    value={inputs[prov.id] || ''}
                    onChange={(e) => setInputs((prev) => ({ ...prev, [prov.id]: e.target.value }))}
                  />
                  <button
                    type="button"
                    className="provider-save-btn"
                    onClick={() => handleSave(prov.id)}
                    disabled={!inputs[prov.id]?.trim()}
                  >
                    Save
                  </button>
                  {isConfigured && (
                    <button
                      type="button"
                      className="provider-remove-btn"
                      onClick={() => handleRemove(prov.id)}
                      title="Remove key"
                    >
                      Clear
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        <footer className="modal-footer">
          <button type="button" className="modal-done-btn" onClick={onClose}>
            Done
          </button>
        </footer>
      </div>
    </div>
  );
}
