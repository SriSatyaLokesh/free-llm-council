import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import RunRail from './RunRail';
import VerdictHero from './VerdictHero';
import ProcessPanel from './ProcessPanel';
import ModelRoster from './ModelRoster';
import { api } from '../api';
import {
  Folder,
  FileText,
  Copy,
  Package,
  Check,
  GroupAILogo,
  LinkIcon,
  UsersIcon,
  SlidersIcon,
  XMark,
} from './icons';
import { shortModel } from '../format';
import { getShareableUrl } from '../utils/url';
import './ChatInterface.css';

export default function ChatInterface({
  conversation,
  projects = [],
  onSendMessage,
  isLoading,
  councilConfig,
  onConfigChange,
  error,
  onOpenReport,
}) {
  const [input, setInput] = useState('');
  const [startedAt, setStartedAt] = useState(null);
  const [idCopied, setIdCopied] = useState(false);
  const [shareCopied, setShareCopied] = useState(false);
  const [isCouncilSidebarOpen, setIsCouncilSidebarOpen] = useState(false);

  const messagesContainerRef = useRef(null);
  const lastUserMsgRef = useRef(null);
  const lastAssistantMsgRef = useRef(null);
  const justSubmittedRef = useRef(false);
  const prevMessageCountRef = useRef(conversation?.messages?.length || 0);
  const prevVerdictRef = useRef(
    Boolean(conversation?.messages?.[conversation?.messages?.length - 1]?.council?.verdict)
  );
  const prevConvIdRef = useRef(conversation?.id);

  /**
   * Scroll within the scoped messages container without triggering
   * viewport-level / document-level scroll jumps in the single-window shell.
   */
  const scrollToElement = (elem, align = 'top') => {
    if (!messagesContainerRef.current || !elem) return;
    const container = messagesContainerRef.current;
    const containerRect = container.getBoundingClientRect();
    const elemRect = elem.getBoundingClientRect();

    if (align === 'top') {
      const targetTop = container.scrollTop + (elemRect.top - containerRect.top) - 16;
      container.scrollTo({
        top: Math.max(0, targetTop),
        behavior: 'smooth',
      });
    } else if (align === 'bottom') {
      const targetTop = container.scrollTop + (elemRect.bottom - containerRect.bottom) + 16;
      container.scrollTo({
        top: Math.max(0, targetTop),
        behavior: 'smooth',
      });
    }
  };

  useEffect(() => {
    if (!conversation) return;

    // Reset when switching to a different conversation
    if (conversation.id !== prevConvIdRef.current) {
      prevConvIdRef.current = conversation.id;
      prevMessageCountRef.current = conversation.messages?.length || 0;
      prevVerdictRef.current = Boolean(
        conversation.messages?.[conversation.messages?.length - 1]?.council?.verdict
      );
      if (conversation.messages?.length > 0 && lastAssistantMsgRef.current) {
        scrollToElement(lastAssistantMsgRef.current, 'top');
      }
      return;
    }

    const currentCount = conversation.messages?.length || 0;
    const lastMsg = conversation.messages?.[currentCount - 1];
    const hasVerdict = Boolean(lastMsg?.role === 'assistant' && lastMsg?.council?.verdict);

    // 1. When a new message is submitted / appended, scroll to show the new exchange
    if (justSubmittedRef.current || currentCount > prevMessageCountRef.current) {
      justSubmittedRef.current = false;
      prevMessageCountRef.current = currentCount;
      if (lastUserMsgRef.current) {
        scrollToElement(lastUserMsgRef.current, 'top');
      } else if (lastAssistantMsgRef.current) {
        scrollToElement(lastAssistantMsgRef.current, 'top');
      }
      return;
    }

    // 2. When the council verdict arrives, smoothly bring the verdict hero into view from its top
    if (hasVerdict && !prevVerdictRef.current) {
      prevVerdictRef.current = true;
      if (lastAssistantMsgRef.current) {
        scrollToElement(lastAssistantMsgRef.current, 'top');
      }
      return;
    }

    prevVerdictRef.current = hasVerdict;
  }, [conversation]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      justSubmittedRef.current = true;
      setStartedAt(Date.now());
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (!conversation) {
    return (
      <div className="chat-interface">
        <div className="empty-state">
          <h2>LLM Council</h2>
          <p>Create a new conversation to get started.</p>
        </div>
      </div>
    );
  }

  const isEmpty = !conversation.messages || conversation.messages.length === 0;
  const activeProject = projects.find((p) => p.id === conversation.project_id);

  const handleCopyId = async () => {
    if (!conversation?.id) return;
    const shareUrl = getShareableUrl(conversation.id);
    try {
      await navigator.clipboard.writeText(shareUrl);
      setIdCopied(true);
      setTimeout(() => setIdCopied(false), 2000);
    } catch {
      navigator.clipboard.writeText(conversation.id);
      setIdCopied(true);
      setTimeout(() => setIdCopied(false), 2000);
    }
  };

  const handleShareDebate = async () => {
    if (!conversation?.id) return;
    const shareUrl = getShareableUrl(conversation.id);
    try {
      await navigator.clipboard.writeText(shareUrl);
      setShareCopied(true);
      setTimeout(() => setShareCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy share link:', err);
    }
  };

  const handleExportReport = () => {
    if (!conversation?.id) return;
    window.open(api.getReportExportUrl(conversation.id), '_blank');
  };

  const handleExportZip = () => {
    if (!conversation?.id) return;
    window.open(api.getZipExportUrl(conversation.id), '_blank');
  };

  return (
    <div className="chat-interface">
      <div className="chat-workspace-main">
        <div className="workspace-header">
          <div className="workspace-breadcrumb">
            {activeProject ? (
              <span className="breadcrumb-folder" title={`Workspace: ${activeProject.name}`}>
                <Folder size={14} className="breadcrumb-icon" />
                <span className="breadcrumb-folder-name">{activeProject.name}</span>
              </span>
            ) : (
              <span className="breadcrumb-independent" title="Standalone deliberation workspace">
                <FileText size={14} className="breadcrumb-icon" />
                <span>Standalone Debate</span>
              </span>
            )}
            <span className="breadcrumb-sep" aria-hidden="true">/</span>
            <h2 className="breadcrumb-title" title={conversation.title || 'New Debate'}>
              {conversation.title || 'New Debate'}
            </h2>
            <button
              type="button"
              className="conv-id-badge"
              onClick={handleCopyId}
              title={`Deliberation Link: ${getShareableUrl(conversation?.id)}\nClick to copy shareable URL`}
            >
              <span className="conv-id-prefix">ID:</span>
              <span className="conv-id-value">{conversation.id ? conversation.id.slice(0, 8) : 'new'}…</span>
              <span className="conv-id-icon">
                {idCopied ? (
                  <>
                    <Check size={12} />
                    <span className="conv-copied-text">URL Copied</span>
                  </>
                ) : (
                  <Copy size={12} />
                )}
              </span>
            </button>
          </div>

          <div className="workspace-actions">
            <button
              type="button"
              className={`export-btn council-sidebar-toggle-btn ${isCouncilSidebarOpen ? 'active' : ''}`}
              onClick={() => setIsCouncilSidebarOpen((v) => !v)}
              title="Toggle Council Models & Configuration Sidebar"
            >
              <UsersIcon size={14} />
              <span>Council ({councilConfig.members?.length || 0})</span>
            </button>
            <button
              type="button"
              className="export-btn share-link-btn"
              onClick={handleShareDebate}
              title="Copy shareable URL for this deliberation"
            >
            {shareCopied ? (
              <>
                <Check size={14} />
                <span>Link Copied</span>
              </>
            ) : (
              <>
                <LinkIcon size={14} />
                <span>Share Debate</span>
              </>
            )}
          </button>
          <button
            type="button"
            className="export-btn export-report-btn"
            onClick={() => onOpenReport && onOpenReport('executive')}
            title="Open interactive deliberation report (Executive Brief & Deep-Dive Matrix)"
          >
            <FileText size={14} />
            <span>Deliberation Report</span>
          </button>
          <button
            type="button"
            className="export-btn export-zip-btn"
            onClick={handleExportZip}
            title="Download full council deliberation package as a .zip (report.md, conversation.json, summary.txt)"
          >
            <Package size={14} />
            <span>Export ZIP</span>
          </button>
        </div>
      </div>

      <div className="messages-container" ref={messagesContainerRef}>
        {isEmpty ? (
          <div className="empty-state">
            <GroupAILogo size={56} className="empty-state-logo" />
            <h2>Start a council</h2>
            <p>
              Bring an idea, a decision, or a design question. Every model available
              in your opencode researches it, argues with the others, and a chairman
              returns a decision with the tradeoffs.
            </p>
          </div>
        ) : (
          conversation.messages.map((msg, index) => {
            const isLastUser = msg.role === 'user' && index >= conversation.messages.length - 2;
            const isLastAssistant = msg.role === 'assistant' && index === conversation.messages.length - 1;

            return msg.role === 'user' ? (
              <div
                key={index}
                className="message-group user-group"
                ref={isLastUser ? lastUserMsgRef : null}
              >
                <div className="user-message">
                  <div className="message-label">You</div>
                  <div className="message-content">
                    <div className="markdown-content">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div
                key={index}
                className="message-group assistant-group"
                ref={isLastAssistant ? lastAssistantMsgRef : null}
              >
                <div className="assistant-message">
                  {msg.loading && Object.values(msg.loading).some(Boolean) && (
                    <RunRail
                      council={msg.council}
                      loading={msg.loading}
                      members={msg.council?.metadata?.members}
                      chairman={msg.council?.metadata?.chairman}
                      startedAt={startedAt}
                      conversationId={conversation?.id}
                    />
                  )}

                  {msg.council?.verdict && (
                    <VerdictHero
                      verdict={msg.council.verdict}
                      compression={msg.council.metadata?.caveman}
                      metadata={msg.council.metadata}
                      conversationId={conversation?.id}
                      onOpenReport={() => onOpenReport && onOpenReport('executive')}
                    />
                  )}

                  <ProcessPanel council={msg.council} />

                  {msg.loading?.verdict && !msg.council?.verdict && (
                    <div className="stage-loading">
                      <span className="spinner" aria-hidden="true" />
                      <span>The chairman is weighing the transcript…</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}

        {error && (
          <div className="stream-error" role="alert">
            <strong>The council run failed.</strong> {error}
          </div>
        )}
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <div className="council-composer-strip">
          <div className="council-composer-info">
            <span className="council-composer-dot" aria-hidden="true" />
            <span className="council-composer-label">Council:</span>
            <span className="council-composer-text">
              {councilConfig.members?.length || 0} models seated
              {councilConfig.chairman && ` · Chair: ${shortModel(councilConfig.chairman)}`}
              {councilConfig.rounds != null && ` · ${councilConfig.rounds} rounds`}
            </span>
          </div>
          <button
            type="button"
            className="council-composer-btn"
            onClick={() => setIsCouncilSidebarOpen((v) => !v)}
            title="Configure council members, reasoning depth, and debate parameters in the sidebar"
          >
            <SlidersIcon size={13} />
            <span>{isCouncilSidebarOpen ? 'Close Sidebar' : 'Configure Council'}</span>
          </button>
        </div>
        <div className="input-row">
          <label className="sr-only" htmlFor="composer">
            Ask the council a question
          </label>
          <textarea
            id="composer"
            className="message-input"
            placeholder="Bring the council an idea, a decision, or a question… (Shift+Enter for a new line)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            rows={3}
          />
          <button
            type="submit"
            className="send-button"
            disabled={!input.trim() || isLoading}
          >
            {isLoading ? 'Running' : 'Send'}
          </button>
        </div>
      </form>
    </div>

    {/* Council Models & Configuration Sidebar */}
    {isCouncilSidebarOpen && (
      <aside className="council-config-sidebar">
        <div className="council-sidebar-header">
          <div className="council-sidebar-title">
            <UsersIcon size={16} />
            <h3>Council Setup</h3>
            <span className="council-sidebar-count-badge">
              {councilConfig.members?.length || 0} Seated
            </span>
          </div>
          <button
            type="button"
            className="council-sidebar-close"
            onClick={() => setIsCouncilSidebarOpen(false)}
            title="Close Council Setup Sidebar"
            aria-label="Close Council Setup Sidebar"
          >
            <XMark size={16} />
          </button>
        </div>
        <div className="council-sidebar-body">
          <ModelRoster
            config={councilConfig}
            onChange={onConfigChange}
            disabled={isLoading}
            evictedModels={
              [...(conversation.messages || [])]
                .reverse()
                .find((m) => m.role === 'assistant')?.council?.metadata?.evicted_models || []
            }
            retiredModels={
              [...(conversation.messages || [])]
                .reverse()
                .find((m) => m.role === 'assistant')?.council?.metadata?.retired_models || []
            }
            isSidebar={true}
          />
        </div>
      </aside>
    )}
  </div>
);
}
