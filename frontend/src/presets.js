/**
 * Council settings presets and auto-reconciliation.
 * Allows persisting chosen council configuration across sessions
 * and automatically adapting if OpenCode models update or deprecate.
 */

const PRESET_KEY = 'llm_council_settings_preset_v1';

export function saveCouncilPreset(config) {
  if (!config) return false;
  try {
    const payload = {
      members: config.members || null,
      chairman: config.chairman || null,
      rounds: config.rounds ?? 2,
      debateMode: config.debateMode || 'full',
      tokenCapPerModel: config.tokenCapPerModel ?? null,
      tokenBudgetTotal: config.tokenBudgetTotal ?? null,
      timeLimitSeconds: config.timeLimitSeconds ?? null,
      modelThinking: config.modelThinking || {},
      savedAt: Date.now(),
    };
    localStorage.setItem(PRESET_KEY, JSON.stringify(payload));
    return true;
  } catch (err) {
    console.error('Failed to save council preset to localStorage:', err);
    return false;
  }
}

export function loadCouncilPreset() {
  try {
    const raw = localStorage.getItem(PRESET_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch (err) {
    console.error('Failed to read council preset from localStorage:', err);
    return null;
  }
}

/**
 * Reconciles a saved preset against the live OpenCode models.
 * If models were updated (e.g. ling-3.0 to ling-3.1), adopts the latest model.
 */
export function reconcilePreset(preset, availableModels, defaultChairman) {
  if (!preset || !availableModels || availableModels.length === 0) {
    return null;
  }

  const availIds = availableModels.map((m) => m.id);
  const idToModel = Object.fromEntries(availableModels.map((m) => [m.id, m]));

  const savedMembers = preset.members || [];
  const newMembers = [];
  const replacementMap = {};

  if (savedMembers.length === 0) {
    newMembers.push(...availIds);
  } else {
    for (const m of savedMembers) {
      if (availIds.includes(m)) {
        newMembers.push(m);
      } else {
        // Fuzzy family match (e.g., 'ling' or 'nemotron')
        const baseKey = (m.split('/').pop() || '').split('-')[0];
        const candidate = availIds.find(
          (aid) => aid.includes(baseKey) && !newMembers.includes(aid)
        );
        if (candidate) {
          newMembers.push(candidate);
          replacementMap[m] = candidate;
        }
      }
    }
  }

  // Ensure minimum quorum
  if (newMembers.length < 2 && availIds.length >= 2) {
    for (const aid of availIds) {
      if (!newMembers.includes(aid)) {
        newMembers.push(aid);
      }
    }
  }

  // Reconcile Chairman
  let chair = preset.chairman;
  if (chair) {
    if (newMembers.includes(chair)) {
      // Preserved
    } else if (replacementMap[chair]) {
      chair = replacementMap[chair];
    } else {
      chair = defaultChairman || newMembers[0] || null;
    }
  } else {
    chair = defaultChairman || null;
  }

  // Reconcile modelThinking
  const savedThinking = preset.modelThinking || {};
  const newThinking = {};
  for (const [m, variant] of Object.entries(savedThinking)) {
    const targetM = replacementMap[m] || m;
    const modelInfo = idToModel[targetM];
    if (modelInfo) {
      const variants = (modelInfo.variants || []).map((v) =>
        typeof v === 'string' ? v : v.id
      );
      if (variants.includes(variant)) {
        newThinking[targetM] = variant;
      } else if (variants.length > 0) {
        newThinking[targetM] = targetM === chair ? variants[variants.length - 1] : variants[0];
      }
    }
  }

  return {
    members: newMembers,
    chairman: chair,
    rounds: preset.rounds ?? 2,
    debateMode: preset.debateMode || 'full',
    tokenCapPerModel: preset.tokenCapPerModel ?? null,
    tokenBudgetTotal: preset.tokenBudgetTotal ?? null,
    timeLimitSeconds: preset.timeLimitSeconds ?? null,
    modelThinking: newThinking,
  };
}
