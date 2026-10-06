import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import { api } from './api';
import './App.css';

function App() {
  const [conversations, setConversations] = useState([]);
  const [projects, setProjects] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [streamError, setStreamError] = useState(null);

  // Council composition, chosen in the roster panel. debateMode is mirrored to
  // the server on change, so the backend can apply it mid-run.
  const [councilConfig, setCouncilConfig] = useState({
    members: null,
    chairman: null,
    rounds: 2,
    debateMode: 'full',
    tokenCapPerModel: null,
    tokenBudgetTotal: null,
    timeLimitSeconds: null,
    modelThinking: null,
  });

  useEffect(() => {
    let cancelled = false;
    api
      .getSettings()
      .then((data) => {
        if (!cancelled) {
          setCouncilConfig((prev) => ({
            ...prev,
            debateMode: data.debateMode,
            tokenCapPerModel: data.tokenCapPerModel ?? prev.tokenCapPerModel,
            tokenBudgetTotal: data.tokenBudgetTotal ?? prev.tokenBudgetTotal,
            timeLimitSeconds: data.timeLimitSeconds ?? prev.timeLimitSeconds,
          }));
        }
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  // Load the conversation list and projects on mount.
  useEffect(() => {
    let cancelled = false;
    api
      .listConversations()
      .then((convs) => {
        if (!cancelled) {
          setConversations(convs);
          if (convs && convs.length > 0) {
            setCurrentConversationId((prev) => prev || convs[0].id);
          } else {
            handleNewConversation();
          }
        }
      })
      .catch((error) => console.error('Failed to load conversations:', error));
    api
      .listProjects()
      .then((projs) => !cancelled && setProjects(projs))
      .catch((error) => console.error('Failed to load projects:', error));
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!currentConversationId) return undefined;
    let cancelled = false;
    api
      .getConversation(currentConversationId)
      .then((conv) => !cancelled && setCurrentConversation(conv))
      .catch((error) => console.error('Failed to load conversation:', error));
    return () => {
      cancelled = true;
    };
  }, [currentConversationId]);

  // Antigravity ergonomics: Cmd/Ctrl + K to start a new deliberation instantly
  useEffect(() => {
    const handleGlobalKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        handleNewConversation();
      }
    };
    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, [currentConversation]);

  /** Refresh the sidebar and projects, e.g. after a run or folder action. */
  function reloadConversations() {
    api
      .listConversations()
      .then(setConversations)
      .catch((error) => console.error('Failed to load conversations:', error));
  }

  function reloadProjects() {
    api
      .listProjects()
      .then(setProjects)
      .catch((error) => console.error('Failed to load projects:', error));
  }

  const discardEmptyCurrent = () => {
    if (currentConversation && (!currentConversation.messages || currentConversation.messages.length === 0)) {
      const emptyId = currentConversation.id;
      setConversations((prev) => prev.filter((c) => c.id !== emptyId));
      api.deleteConversation(emptyId).catch(() => {});
    }
  };

  const handleNewConversation = async (projectId = null) => {
    // If current conversation is already an empty draft
    if (currentConversation && (!currentConversation.messages || currentConversation.messages.length === 0)) {
      if (currentConversation.project_id === projectId) return;
      try {
        const updated = await api.updateConversation(currentConversation.id, {
          project_id: projectId,
          unlink_project: !projectId,
        });
        setCurrentConversation(updated);
        reloadConversations();
        reloadProjects();
        return;
      } catch {
        // Fallback to discard & create
      }
    }
    // Discard any existing empty draft before creating a new one
    discardEmptyCurrent();
    try {
      const newConv = await api.createConversation(projectId);
      setCurrentConversation(newConv);
      setCurrentConversationId(newConv.id);
      reloadProjects();
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const handleCreateProject = async (name, description = '') => {
    try {
      await api.createProject(name, description);
      reloadProjects();
    } catch (error) {
      console.error('Failed to create project:', error);
      alert(`Failed to create project: ${error.message}`);
    }
  };

  const handleRenameProject = async (projectId, name) => {
    try {
      await api.updateProject(projectId, { name });
      reloadProjects();
    } catch (error) {
      console.error('Failed to rename project:', error);
      alert(`Failed to rename project: ${error.message}`);
    }
  };

  const handleDeleteProject = async (projectId) => {
    try {
      await api.deleteProject(projectId);
      reloadProjects();
      reloadConversations();
      if (currentConversation?.project_id === projectId) {
        setCurrentConversation((prev) => (prev ? { ...prev, project_id: null } : prev));
      }
    } catch (error) {
      console.error('Failed to delete project:', error);
      alert(`Failed to delete project: ${error.message}`);
    }
  };

  const handleMoveConversation = async (conversationId, targetProjectId) => {
    try {
      const updated = await api.updateConversation(conversationId, {
        project_id: targetProjectId,
        unlink_project: !targetProjectId,
      });
      if (currentConversationId === conversationId) {
        setCurrentConversation(updated);
      }
      reloadConversations();
      reloadProjects();
    } catch (error) {
      console.error('Failed to move conversation:', error);
      alert(`Failed to move conversation: ${error.message}`);
    }
  };

  const handleRenameConversation = async (conversationId, title) => {
    try {
      await api.renameConversation(conversationId, title);
      setCurrentConversation((prev) =>
        prev && prev.id === conversationId ? { ...prev, title } : prev
      );
      reloadConversations();
    } catch (error) {
      console.error('Failed to rename conversation:', error);
      alert(`Failed to rename conversation: ${error.message}`);
    }
  };

  const handleArchiveConversation = async (conversationId, archived = true) => {
    try {
      await api.archiveConversation(conversationId, archived);
      reloadConversations();
      if (currentConversationId === conversationId && archived) {
        // If archived active conversation, select another active one if available
        const remaining = conversations.filter((c) => c.id !== conversationId && !c.archived);
        if (remaining.length > 0) {
          handleSelectConversation(remaining[0].id);
        }
      }
    } catch (error) {
      console.error('Failed to update archive status:', error);
      alert(`Failed to update archive status: ${error.message}`);
    }
  };

  const handleSelectConversation = (id) => {
    if (id === currentConversationId) return;
    discardEmptyCurrent();
    setCurrentConversationId(id);
  };

  const handleConfigChange = (patch) => {
    setCouncilConfig((prev) => ({ ...prev, ...patch }));
  };

  /**
   * Patch the streaming assistant message.
   *
   * The nested council/loading objects are copied rather than mutated, so React
   * actually sees the change and re-renders the affected stage.
   */
  const patchLast = (fn) => {
    setCurrentConversation((prev) => {
      if (!prev) return prev;
      const messages = [...prev.messages];
      const last = messages[messages.length - 1];
      if (!last || last.role !== 'assistant') return prev;

      const blank = {
        positions: [],
        debate: [],
        review: [],
        aggregate: [],
        verdict: null,
        metadata: {},
      };
      const base = {
        ...last,
        council: {
          ...blank,
          ...(last.council || {}),
          metadata: { ...(last.council?.metadata || {}) },
        },
        loading: {
          positions: false,
          debate: false,
          review: false,
          verdict: false,
          ...(last.loading || {}),
        },
      };

      messages[messages.length - 1] = fn(base);
      return { ...prev, messages };
    });
  };

  const handleSendMessage = async (content) => {
    if (!currentConversationId) return;

    setIsLoading(true);
    setStreamError(null);

    const userMessage = { role: 'user', content };
    const assistantMessage = {
      role: 'assistant',
      council: {
        positions: [],
        debate: [],
        review: [],
        aggregate: [],
        verdict: null,
        metadata: {},
      },
      loading: { positions: true, debate: false, review: false, verdict: false },
    };

    setCurrentConversation((prev) => ({
      ...prev,
      messages: [...prev.messages, userMessage, assistantMessage],
    }));

    setConversations((prev) => {
      if (prev.some((c) => c.id === currentConversationId)) return prev;
      return [
        {
          id: currentConversationId,
          created_at: new Date().toISOString(),
          title: content.slice(0, 40) || 'New Conversation',
          message_count: 1,
          project_id: currentConversation?.project_id || null,
        },
        ...prev,
      ];
    });

    const options = {
      members: councilConfig.members?.length ? councilConfig.members : null,
      chairman: councilConfig.chairman,
      rounds: councilConfig.rounds,
      token_cap_per_model: councilConfig.tokenCapPerModel,
      token_budget_total: councilConfig.tokenBudgetTotal,
      time_limit_seconds: councilConfig.timeLimitSeconds,
      model_thinking: councilConfig.modelThinking,
    };

    try {
      await api.sendMessageStream(currentConversationId, content, options, (type, event) => {
        switch (type) {
          case 'roster':
            patchLast((msg) => {
              msg.council.metadata.members = event.data.members;
              msg.council.metadata.chairman = event.data.chairman;
              return msg;
            });
            break;

          case 'positions_complete':
            patchLast((msg) => {
              msg.council.positions = event.data || [];
              msg.loading.positions = false;
              msg.loading.debate = true;
              return msg;
            });
            break;

          case 'debate_round_complete':
            patchLast((msg) => {
              msg.council.debate = [...msg.council.debate, event.data];
              return msg;
            });
            break;

          case 'review_complete':
            patchLast((msg) => {
              // The backend now sends {reviews, cavemanLevel, tokens}.
              msg.council.review = event.data?.reviews || [];
              msg.council.reviewMeta = {
                cavemanLevel: event.data?.cavemanLevel,
                tokens: event.data?.tokens,
              };
              msg.loading.review = false;
              msg.loading.verdict = true;
              return msg;
            });
            break;

          case 'aggregate_complete':
            patchLast((msg) => {
              msg.council.aggregate = event.data || [];
              msg.council.metadata.aggregate_rankings = event.data || [];
              return msg;
            });
            break;

          case 'verdict_complete':
            patchLast((msg) => {
              msg.council.verdict = event.data;
              msg.loading.verdict = false;
              return msg;
            });
            break;

          case 'model_evicted':
            patchLast((msg) => {
              const prevEvicted = msg.council.metadata.evicted_models || [];
              msg.council.metadata.evicted_models = [...prevEvicted, event.data];
              return msg;
            });
            break;

          case 'model_retired':
            patchLast((msg) => {
              const prevRetired = msg.council.metadata.retired_models || [];
              msg.council.metadata.retired_models = [...prevRetired, event.data];
              return msg;
            });
            break;

          case 'debate_concluded_early':
            patchLast((msg) => {
              msg.council.metadata.early_conclusion_reason = event.data?.reason;
              msg.council.metadata.early_conclusion = event.data;
              return msg;
            });
            break;

          case 'human_guidance_injected':
            patchLast((msg) => {
              const prevGuidance = msg.council.metadata.injected_guidance || [];
              msg.council.metadata.injected_guidance = [...prevGuidance, event.data];
              return msg;
            });
            break;

          case 'title_complete':
            reloadConversations();
            reloadProjects();
            break;

          case 'error':
            setStreamError(event.message);
            patchLast((msg) => {
              msg.loading = {
                positions: false,
                debate: false,
                review: false,
                verdict: false,
              };
              return msg;
            });
            setIsLoading(false);
            break;

          case 'complete':
            reloadConversations();
            reloadProjects();
            setIsLoading(false);
            break;

          default:
            break;
        }
      });
    } catch (error) {
      console.error('Failed to send message:', error);
      setStreamError(error.message);
      setCurrentConversation((prev) => ({
        ...prev,
        messages: prev.messages.slice(0, -2),
      }));
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Sidebar
        conversations={conversations}
        projects={projects}
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        onCreateProject={handleCreateProject}
        onRenameProject={handleRenameProject}
        onDeleteProject={handleDeleteProject}
        onMoveConversation={handleMoveConversation}
        onRenameConversation={handleRenameConversation}
        onArchiveConversation={handleArchiveConversation}
        onKeysUpdated={() => {
          api.getModels().catch(() => {});
        }}
      />
      <ChatInterface
        conversation={currentConversation}
        projects={projects}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        councilConfig={councilConfig}
        onConfigChange={handleConfigChange}
        error={streamError}
      />
    </div>
  );
}

export default App;
