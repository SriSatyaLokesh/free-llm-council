/**
 * Small formatting helpers shared by the council stage components.
 */

/** "opencode/muse-spark-1.3-contributor-free" -> "muse-spark-1.3" */
export function shortModel(model) {
  if (!model) return '';
  const name = model.split('/').pop() || model;
  return name
    .replace(/-contributor-free$/, '')
    .replace(/-preview-free$/, '')
    .replace(/-free$/, '')
    .replace(/-preview$/, '')
    .replace(/-contributor$/, '');
}

/** Human readable token count, e.g. 12823 -> "12.8k" */
export function formatTokens(tokens) {
  if (!tokens) return null;
  const total = (tokens.input || 0) + (tokens.output || 0);
  if (!total) return null;
  if (total < 1000) return `${total} tok`;
  if (total < 10000) return `${(total / 1000).toFixed(1)}k tok`;
  return `${Math.round(total / 1000)}k tok`;
}

/** Trim a URL down to something that fits in a chip. */
export function shortUrl(url) {
  if (!url) return null;
  try {
    const parsed = new URL(url);
    const path = parsed.pathname === '/' ? '' : parsed.pathname;
    const label = `${parsed.hostname.replace(/^www\./, '')}${path}`;
    return label.length > 42 ? `${label.slice(0, 40)}…` : label;
  } catch {
    return url.length > 42 ? `${url.slice(0, 40)}…` : url;
  }
}

/** A one-line summary of what a tool call did, for the trace chips. */
export function toolCallLabel(call) {
  const input = call.input || {};
  if (call.name === 'webfetch') return shortUrl(input.url) || 'fetch';
  if (call.name === 'websearch') return input.query || 'search';
  if (call.name === 'read') return input.filePath || input.path || 'read';
  if (call.name === 'grep') return input.pattern || 'grep';
  if (call.name === 'glob') return input.pattern || 'glob';
  if (call.name === 'list') return input.path || 'list';
  return call.name;
}
