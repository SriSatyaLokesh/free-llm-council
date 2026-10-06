import { useState, useEffect, useMemo } from 'react';
import { api } from '../api';
import { XMark } from './icons';
import './ProviderKeyModal.css';

const PROVIDERS = [
  {
    id: 'openrouter',
    label: 'OpenRouter',
    category: 'Aggregator',
    placeholder: 'sk-or-v1-...',
    docs: 'https://openrouter.ai/keys',
    description: 'Access 200+ models including Claude 3.5 Sonnet, DeepSeek R1, Llama 3.3, and GPT-4o.',
  },
  {
    id: 'openai',
    label: 'OpenAI',
    category: 'Frontier',
    placeholder: 'sk-proj-...',
    docs: 'https://platform.openai.com/api-keys',
    description: 'Direct access to GPT-4o, GPT-4o-mini, o1, and o3-mini reasoning models.',
  },
  {
    id: 'anthropic',
    label: 'Anthropic',
    category: 'Frontier',
    placeholder: 'sk-ant-api03-...',
    docs: 'https://console.anthropic.com/settings/keys',
    description: 'Direct access to Claude 3.5 Sonnet, Claude 3.7 Sonnet, and Haiku.',
  },
  {
    id: 'google',
    label: 'Google Gemini',
    category: 'Frontier',
    placeholder: 'AIzaSy...',
    docs: 'https://aistudio.google.com/app/apikey',
    description: 'Direct access to Gemini 2.0 Flash, Gemini 1.5 Pro, and experimental thinking models.',
  },
  {
    id: 'groq',
    label: 'Groq',
    category: 'High-Speed',
    placeholder: 'gsk_...',
    docs: 'https://console.groq.com/keys',
    description: 'Ultra-fast LPU inference for Llama 3.3 70B, DeepSeek R1 Distill, and Mixtral.',
  },
  {
    id: 'deepseek',
    label: 'DeepSeek',
    category: 'Frontier',
    placeholder: 'sk-...',
    docs: 'https://platform.deepseek.com/api_keys',
    description: 'Direct low-cost access to DeepSeek V3 and DeepSeek R1 reasoning models.',
  },
  {
    id: 'mistral',
    label: 'Mistral AI',
    category: 'Open Weights',
    placeholder: '...',
    docs: 'https://console.mistral.ai/api-keys',
    description: 'Direct access to Mistral Large 2, Codestral, and Pixtral.',
  },
  {
    id: 'xai',
    label: 'xAI (Grok)',
    category: 'Frontier',
    placeholder: 'xai-...',
    docs: 'https://console.x.ai/',
    description: 'Direct access to Grok 2, Grok 2 Vision, and Grok beta reasoning.',
  },
  {
    id: 'together',
    label: 'Together AI',
    category: 'High-Speed',
    placeholder: '...',
    docs: 'https://api.together.ai/settings/api-keys',
    description: 'Accelerated cloud inference for open-weights Llama 3.3, Qwen 2.5, and DeepSeek.',
  },
  {
    id: 'cohere',
    label: 'Cohere',
    category: 'Enterprise',
    placeholder: '...',
    docs: 'https://dashboard.cohere.com/api-keys',
    description: 'Direct access to Command R+, Command R, and enterprise reasoning models.',
  },
];

const CATEGORIES = ['All', 'Frontier', 'High-Speed', 'Aggregator', 'Open Weights', 'Enterprise'];

export default function ProviderKeyModal({ isOpen, onClose, onKeysUpdated }) {
  const [keysStatus, setKeysStatus] = useState({});
  const [inputs, setInputs] = useState({});
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

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

  const filteredProviders = useMemo(() => {
    return PROVIDERS.filter((prov) => {
      const matchesCategory =
        selectedCategory === 'All' || prov.category === selectedCategory;
      const query = searchQuery.toLowerCase().trim();
      const matchesQuery =
        !query ||
        prov.label.toLowerCase().includes(query) ||
        prov.description.toLowerCase().includes(query) ||
        prov.id.toLowerCase().includes(query);
      return matchesCategory && matchesQuery;
    });
  }, [searchQuery, selectedCategory]);

  const configuredCount = useMemo(() => {
    return Object.values(keysStatus).filter((s) => s?.configured).length;
  }, [keysStatus]);

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <header className="modal-header">
          <div>
            <div className="modal-title-row">
              <h2 id="modal-title">Provider API Keys</h2>
              {configuredCount > 0 && (
                <span className="modal-configured-badge">
                  {configuredCount} configured
                </span>
              )}
            </div>
            <p className="modal-subtitle">
              Local OpenCode models run 100% free with zero config. Seat optional frontier and high-speed cloud models alongside them.
            </p>
          </div>
          <button type="button" className="modal-close-btn" onClick={onClose} aria-label="Close dialog">
            <XMark size={14} />
          </button>
        </header>

        {statusMsg && <div className="modal-alert modal-alert-success">{statusMsg}</div>}
        {errorMsg && <div className="modal-alert modal-alert-error">{errorMsg}</div>}

        <div className="modal-filters">
          <input
            type="text"
            className="provider-search-input"
            placeholder="Search providers or models (Gemini, Groq, Claude, DeepSeek…)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <div className="category-chips">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                type="button"
                className={`category-chip ${selectedCategory === cat ? 'active' : ''}`}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="provider-list">
          {filteredProviders.length === 0 ? (
            <div className="providers-empty">
              No providers match "{searchQuery}"
            </div>
          ) : (
            filteredProviders.map((prov) => {
              const status = keysStatus[prov.id];
              const isConfigured = Boolean(status?.configured);
              const preview = status?.preview;

              return (
                <div key={prov.id} className="provider-card">
                  <div className="provider-header">
                    <div className="provider-info">
                      <span className="provider-name">{prov.label}</span>
                      <span className="provider-category-tag">{prov.category}</span>
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
            })
          )}
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
