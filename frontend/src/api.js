/**
 * API client for the LLM Council backend.
 */

const API_BASE = 'http://localhost:8001';

export const api = {
  /**
   * List all conversations.
   */
  async listConversations() {
    const response = await fetch(`${API_BASE}/api/conversations`);
    if (!response.ok) {
      throw new Error('Failed to list conversations');
    }
    return response.json();
  },

  /**
   * Fetch the council roster from opencode.
   * Returns { models, defaultChairman, defaultRounds }.
   */
  async getModels() {
    const response = await fetch(`${API_BASE}/api/models`);
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to load models from opencode');
    }
    return response.json();
  },

  /**
   * Fetch live council settings, including Caveman install status.
   * Returns { debateMode, caveman: { installed, levels, levelDescriptions, ... } }.
   */
  async getSettings() {
    const response = await fetch(`${API_BASE}/api/settings`);
    if (!response.ok) {
      throw new Error('Failed to load settings');
    }
    return response.json();
  },

  /**
   * Change the compression level. Takes effect on the next debate round,
   * including mid-run.
   */
  async updateSettings(patch) {
    const response = await fetch(`${API_BASE}/api/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patch),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to update settings');
    }
    return response.json();
  },

  /**
   * Check connection to local OpenCode server.
   */
  async getHealth() {
    const response = await fetch(`${API_BASE}/api/health`);
    return response.json();
  },

  /**
   * Get configured provider API key statuses (redacted).
   */
  async getProviderKeys() {
    const response = await fetch(`${API_BASE}/api/providers/keys`);
    if (!response.ok) {
      throw new Error('Failed to load provider key statuses');
    }
    return response.json();
  },

  /**
   * Update or remove a provider API key.
   */
  async updateProviderKey(provider, key) {
    const response = await fetch(`${API_BASE}/api/providers/keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider, key }),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to update provider key');
    }
    return response.json();
  },

  /**
   * List all projects.
   */
  async listProjects() {
    const response = await fetch(`${API_BASE}/api/projects`);
    if (!response.ok) {
      throw new Error('Failed to list projects');
    }
    return response.json();
  },

  /**
   * Create a new project workspace folder.
   */
  async createProject(name, description = '') {
    const response = await fetch(`${API_BASE}/api/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description }),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to create project');
    }
    return response.json();
  },

  /**
   * Update a project name or description.
   */
  async updateProject(projectId, patch) {
    const response = await fetch(`${API_BASE}/api/projects/${projectId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patch),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to update project');
    }
    return response.json();
  },

  /**
   * Delete a project workspace folder.
   */
  async deleteProject(projectId) {
    const response = await fetch(`${API_BASE}/api/projects/${projectId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete project');
    }
    return response.json();
  },

  /**
   * Create a new conversation.
   */
  async createConversation(projectId = null) {
    const response = await fetch(`${API_BASE}/api/conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(projectId ? { project_id: projectId } : {}),
    });
    if (!response.ok) {
      throw new Error('Failed to create conversation');
    }
    return response.json();
  },

  /**
   * Update a conversation (e.g., project assignment, title, or archive status).
   */
  async updateConversation(conversationId, patch) {
    const response = await fetch(`${API_BASE}/api/conversations/${conversationId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patch),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to update conversation');
    }
    return response.json();
  },

  /**
   * Rename a conversation title.
   */
  async renameConversation(conversationId, title) {
    return this.updateConversation(conversationId, { title });
  },

  /**
   * Archive or unarchive a conversation.
   */
  async archiveConversation(conversationId, archived = true) {
    return this.updateConversation(conversationId, { archived });
  },

  /**
   * Get a specific conversation.
   */
  async getConversation(conversationId) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}`
    );
    if (!response.ok) {
      throw new Error('Failed to get conversation');
    }
    return response.json();
  },

  /**
   * Delete a conversation by ID.
   */
  async deleteConversation(conversationId) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}`,
      { method: 'DELETE' }
    );
    if (!response.ok) {
      throw new Error('Failed to delete conversation');
    }
    return response.json();
  },

  /**
   * Prune empty abandoned conversations (0 messages).
   */
  async pruneEmptyConversations() {
    const response = await fetch(
      `${API_BASE}/api/conversations/prune-empty`,
      { method: 'POST' }
    );
    if (!response.ok) {
      throw new Error('Failed to prune empty conversations');
    }
    return response.json();
  },

  /**
   * Download a conversation as a markdown report (executive or detailed).
   */
  getReportExportUrl(conversationId, format = 'executive') {
    return `${API_BASE}/api/conversations/${conversationId}/export/report?format=${encodeURIComponent(format)}`;
  },

  /**
   * Fetch pre-rendered executive and detailed reports for in-app viewing.
   */
  async getReports(conversationId) {
    const response = await fetch(`${API_BASE}/api/conversations/${conversationId}/reports`);
    if (!response.ok) {
      throw new Error('Failed to load deliberation reports');
    }
    return response.json();
  },

  /**
   * Download a conversation as a zip archive.
   */
  getZipExportUrl(conversationId) {
    return `${API_BASE}/api/conversations/${conversationId}/export/zip`;
  },

  /**
   * Send a message in a conversation.
   */
  async sendMessage(conversationId, content, options = {}) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}/message`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content, ...options }),
      }
    );
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to send message');
    }
    return response.json();
  },

  /**
   * Inject human operator guidance or resources into an active debate.
   */
  async steerDebate(conversationId, message, resources = []) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}/steer`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, resources }),
      }
    );
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to inject steering guidance');
    }
    return response.json();
  },

  /**
   * Send a message and receive streaming updates.
   * @param {string} conversationId - The conversation ID
   * @param {string} content - The message content
   * @param {object} options - { members, chairman, rounds }
   * @param {function} onEvent - Callback function for each event: (eventType, event) => void
   * @returns {Promise<void>}
   */
  async sendMessageStream(conversationId, content, options, onEvent) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}/message/stream`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content, ...options }),
      }
    );

    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || 'Failed to send message');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // SSE frames are separated by a blank line. Buffer across chunk
      // boundaries so a split "data:" line is not lost.
      const frames = buffer.split('\n\n');
      buffer = frames.pop() ?? '';

      for (const frame of frames) {
        for (const line of frame.split('\n')) {
          if (!line.startsWith('data:')) continue;
          const payload = line.slice(5).trim();
          if (!payload) continue;
          try {
            const event = JSON.parse(payload);
            onEvent(event.type, event);
          } catch (e) {
            console.error('Failed to parse SSE event:', e);
          }
        }
      }
    }
  },
};
