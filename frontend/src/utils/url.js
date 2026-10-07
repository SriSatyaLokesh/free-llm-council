/**
 * URL Routing & Deep-Linking Utilities for Deliberations and Reports.
 *
 * Supports deep-linking, browser history navigation (popstate),
 * clean query parameters (?c=<id>&report=<executive|detailed>),
 * and shareable URLs across private and hosted deployments.
 */

export function getUrlDeliberationState() {
  if (typeof window === 'undefined') {
    return { id: null, report: null };
  }

  const searchParams = new URLSearchParams(window.location.search);
  let id =
    searchParams.get('c') ||
    searchParams.get('session') ||
    searchParams.get('debate') ||
    searchParams.get('chat') ||
    searchParams.get('id');

  let report = searchParams.get('report');

  // Fallback to hash route: e.g. #/c/<id> or #<id>
  if (!id && window.location.hash) {
    const cleanHash = window.location.hash.replace(/^#\/?/, '');
    const [pathPart, queryPart] = cleanHash.split('?');
    if (pathPart.startsWith('c/')) {
      id = pathPart.replace('c/', '');
    } else if (pathPart.length >= 8 && !pathPart.includes('/')) {
      id = pathPart;
    }

    if (queryPart) {
      const hashParams = new URLSearchParams(queryPart);
      if (!id) id = hashParams.get('c') || hashParams.get('session');
      if (!report) report = hashParams.get('report');
    }
  }

  // Fallback to pathname: e.g. /c/<id>
  if (!id && window.location.pathname.startsWith('/c/')) {
    id = window.location.pathname.replace('/c/', '').split('/')[0];
  }

  const validReport =
    report === 'detailed'
      ? 'detailed'
      : report === 'executive' || report === 'true' || report === '1'
      ? 'executive'
      : null;

  return { id: id ? id.trim() : null, report: validReport };
}

export function updateBrowserUrl(conversationId, reportMode = null, replace = false) {
  if (typeof window === 'undefined') return;

  const url = new URL(window.location.href);

  if (conversationId) {
    url.searchParams.set('c', conversationId);
    // Purge redundant aliases to keep URL clean and canonical
    url.searchParams.delete('session');
    url.searchParams.delete('debate');
    url.searchParams.delete('chat');
    url.searchParams.delete('id');
  } else {
    url.searchParams.delete('c');
  }

  if (reportMode) {
    url.searchParams.set('report', reportMode === 'detailed' ? 'detailed' : 'executive');
  } else {
    url.searchParams.delete('report');
  }

  const targetPathAndQuery = url.pathname + (url.search ? url.search : '') + (url.hash ? url.hash : '');

  const currentPathAndQuery =
    window.location.pathname +
    (window.location.search ? window.location.search : '') +
    (window.location.hash ? window.location.hash : '');

  if (targetPathAndQuery !== currentPathAndQuery) {
    const statePayload = { conversationId, reportMode };
    if (replace) {
      window.history.replaceState(statePayload, '', targetPathAndQuery);
    } else {
      window.history.pushState(statePayload, '', targetPathAndQuery);
    }
  }
}

export function getShareableUrl(conversationId, reportMode = null) {
  if (typeof window === 'undefined') return '';

  const originAndPath = window.location.origin + window.location.pathname;
  const url = new URL(originAndPath);

  if (conversationId) {
    url.searchParams.set('c', conversationId);
  }

  if (reportMode) {
    url.searchParams.set('report', reportMode === 'detailed' ? 'detailed' : 'executive');
  }

  return url.toString();
}
