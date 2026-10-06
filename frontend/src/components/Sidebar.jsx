import { useState, useEffect } from 'react';
import { api } from '../api';
import ProviderKeyModal from './ProviderKeyModal';
import {
  Chevron,
  Check,
  Folder,
  FolderPlus,
  FileText,
  Archive,
  ArchiveRestore,
  Pencil,
  Trash,
  Copy,
  Package,
  Move,
  Key,
  Plus,
  XMark,
  GroupAILogo,
} from './icons';
import './Sidebar.css';

export default function Sidebar({
  conversations = [],
  projects = [],
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onCreateProject,
  onRenameProject,
  onDeleteProject,
  onMoveConversation,
  onRenameConversation,
  onArchiveConversation,
  onKeysUpdated,
}) {
  const [health, setHealth] = useState(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [keyModalOpen, setKeyModalOpen] = useState(false);

  // Project UI state
  const [collapsedProjects, setCollapsedProjects] = useState({});
  const [isCreatingProject, setIsCreatingProject] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');
  const [editingProjectId, setEditingProjectId] = useState(null);
  const [editingProjectName, setEditingProjectName] = useState('');

  // Conversation UI state (Rename, Move, Archive)
  const [editingConvId, setEditingConvId] = useState(null);
  const [editingConvTitle, setEditingConvTitle] = useState('');
  const [activeMoveMenuConvId, setActiveMoveMenuConvId] = useState(null);
  const [copiedConvId, setCopiedConvId] = useState(null);
  const [showArchived, setShowArchived] = useState(false);

  const handleCopyConvId = (id, e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(id);
    setCopiedConvId(id);
    setTimeout(() => setCopiedConvId(null), 2000);
  };

  const fetchHealth = () => {
    api
      .getHealth()
      .then((data) => setHealth(data))
      .catch((err) => setHealth({ status: 'error', error: err.message }))
      .finally(() => setHealthLoading(false));
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const isOk = health?.status === 'ok' && health?.opencode?.status === 'connected';

  const toggleFolder = (projectId) => {
    setCollapsedProjects((prev) => ({
      ...prev,
      [projectId]: !prev[projectId],
    }));
  };

  const handleStartCreateProject = () => {
    setIsCreatingProject(true);
    setNewProjectName('');
    setNewProjectDesc('');
  };

  const handleCancelCreateProject = () => {
    setIsCreatingProject(false);
    setNewProjectName('');
    setNewProjectDesc('');
  };

  const handleConfirmCreateProject = async (e) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;
    if (onCreateProject) {
      await onCreateProject(newProjectName.trim(), newProjectDesc.trim());
    }
    setIsCreatingProject(false);
    setNewProjectName('');
    setNewProjectDesc('');
  };

  const handleStartRenameProject = (project, e) => {
    e.stopPropagation();
    setEditingProjectId(project.id);
    setEditingProjectName(project.name);
  };

  const handleSaveRenameProject = async (projectId, e) => {
    e.preventDefault();
    e.stopPropagation();
    if (editingProjectName.trim() && onRenameProject) {
      await onRenameProject(projectId, editingProjectName.trim());
    }
    setEditingProjectId(null);
  };

  const handleDeleteProjectClick = async (project, e) => {
    e.stopPropagation();
    const confirmMsg = `Delete project "${project.name}"?\nAssociated debates will be kept and reverted to Independent Standalone debates.`;
    if (window.confirm(confirmMsg) && onDeleteProject) {
      await onDeleteProject(project.id);
    }
  };

  const handleMoveChange = async (convId, targetProjectId) => {
    setActiveMoveMenuConvId(null);
    if (onMoveConversation) {
      await onMoveConversation(convId, targetProjectId === 'independent' ? null : targetProjectId);
    }
  };

  const handleStartRenameConv = (conv, e) => {
    e.stopPropagation();
    setEditingConvId(conv.id);
    setEditingConvTitle(conv.title || 'New Debate');
  };

  const handleSaveRenameConv = async (convId, e) => {
    e.preventDefault();
    e.stopPropagation();
    if (editingConvTitle.trim() && onRenameConversation) {
      await onRenameConversation(convId, editingConvTitle.trim());
    }
    setEditingConvId(null);
  };

  const handleCancelRenameConv = (e) => {
    e.stopPropagation();
    setEditingConvId(null);
    setEditingConvTitle('');
  };

  const handleToggleArchiveConv = async (convId, isCurrentlyArchived, e) => {
    e.stopPropagation();
    if (onArchiveConversation) {
      await onArchiveConversation(convId, !isCurrentlyArchived);
    }
  };

  // Partition active vs archived
  const activeConversations = conversations.filter((c) => !c.archived);
  const archivedConversations = conversations.filter((c) => !!c.archived);
  const independentConversations = activeConversations.filter((c) => !c.project_id);

  // Render helper for single conversation row
  const renderConversationRow = (conv, currentFolderId = null) => {
    const isEditing = editingConvId === conv.id;
    const isMoveOpen = activeMoveMenuConvId === conv.id;

    return (
      <div
        key={conv.id}
        className={`conversation-row ${conv.id === currentConversationId ? 'active' : ''} ${conv.archived ? 'archived-row' : ''}`}
      >
        {isEditing ? (
          <form className="inline-rename-form" onSubmit={(e) => handleSaveRenameConv(conv.id, e)}>
            <input
              type="text"
              className="rename-input"
              value={editingConvTitle}
              onChange={(e) => setEditingConvTitle(e.target.value)}
              autoFocus
              onClick={(e) => e.stopPropagation()}
            />
            <button
              type="submit"
              className="rename-save-btn"
              onClick={(e) => e.stopPropagation()}
              title="Save name"
            >
              <Check size={12} />
            </button>
            <button
              type="button"
              className="rename-cancel-btn"
              onClick={handleCancelRenameConv}
              title="Cancel"
            >
              <XMark size={12} />
            </button>
          </form>
        ) : (
          <button
            type="button"
            className="conversation-item-btn"
            onClick={() => onSelectConversation(conv.id)}
          >
            <span className="conversation-title">{conv.title || 'New Debate'}</span>
            <span className="conversation-meta">
              {conv.message_count} msg{conv.message_count === 1 ? '' : 's'}
              {conv.archived && <span className="archived-meta-badge">archived</span>}
            </span>
          </button>
        )}

        <div className="conv-actions-group">
          <button
            type="button"
            className="conv-icon-btn"
            title={`Copy ID (${conv.id})`}
            onClick={(e) => handleCopyConvId(conv.id, e)}
          >
            {copiedConvId === conv.id ? <Check size={12} /> : <Copy size={12} />}
          </button>

          <a
            href={api.getZipExportUrl(conv.id)}
            download
            className="conv-icon-btn"
            title="Download deliberation as ZIP"
            onClick={(e) => e.stopPropagation()}
          >
            <Package size={12} />
          </a>

          <button
            type="button"
            className="conv-icon-btn"
            title="Rename debate"
            onClick={(e) => handleStartRenameConv(conv, e)}
          >
            <Pencil size={12} />
          </button>

          <button
            type="button"
            className="conv-icon-btn"
            title={conv.archived ? 'Restore / Unarchive debate' : 'Archive debate'}
            onClick={(e) => handleToggleArchiveConv(conv.id, conv.archived, e)}
          >
            {conv.archived ? <ArchiveRestore size={12} /> : <Archive size={12} />}
          </button>

          <div className="conv-move-container">
            <button
              type="button"
              className="conv-move-btn"
              title="Move debate into a project folder or standalone"
              onClick={(e) => {
                e.stopPropagation();
                setActiveMoveMenuConvId(isMoveOpen ? null : conv.id);
              }}
            >
              <Move size={12} />
            </button>
            {isMoveOpen && (
              <div className="move-dropdown-menu" onClick={(e) => e.stopPropagation()}>
                <div className="move-dropdown-header">Move debate to:</div>
                <button
                  type="button"
                  className={`move-dropdown-item ${!conv.project_id ? 'current-dest' : ''}`}
                  disabled={!conv.project_id}
                  onClick={() => handleMoveChange(conv.id, 'independent')}
                >
                  <FileText size={12} /> Standalone Debate {!conv.project_id ? '(current)' : ''}
                </button>
                {projects.map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    className={`move-dropdown-item ${p.id === conv.project_id ? 'current-dest' : ''}`}
                    disabled={p.id === conv.project_id}
                    onClick={() => handleMoveChange(conv.id, p.id)}
                  >
                    <Folder size={12} /> {p.name} {p.id === conv.project_id ? '(current)' : ''}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="sidebar-brand-title">
            <GroupAILogo size={22} className="sidebar-brand-logo" />
            <h1>Free LLM Council</h1>
          </div>
        </div>

        <div className="sidebar-action-row">
          <button
            type="button"
            className="new-debate-btn"
            onClick={() => onNewConversation(null)}
            title="Start a new debate (Ctrl/Cmd + K)"
          >
            <Plus size={15} />
            <span>New Debate</span>
          </button>
          <button
            type="button"
            className="new-folder-action-btn"
            onClick={handleStartCreateProject}
            title="Create new workspace folder"
            aria-label="Create new workspace folder"
          >
            <FolderPlus size={15} />
          </button>
        </div>
      </div>

      {isCreatingProject && (
        <form className="inline-project-form" onSubmit={handleConfirmCreateProject}>
          <div className="project-form-title">New Project Workspace</div>
          <input
            type="text"
            className="project-name-input"
            placeholder="Project name (e.g. Distributed DBs)"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            autoFocus
            required
          />
          <input
            type="text"
            className="project-desc-input"
            placeholder="Optional description"
            value={newProjectDesc}
            onChange={(e) => setNewProjectDesc(e.target.value)}
          />
          <div className="project-form-actions">
            <button type="button" className="btn-secondary" onClick={handleCancelCreateProject}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={!newProjectName.trim()}>
              Create
            </button>
          </div>
        </form>
      )}

      <div className="conversation-list">
        {/* Projects / Workspace Folders Section */}
        <div className="sidebar-section">
          <div className="section-header">
            <span className="section-title">PROJECT WORKSPACES</span>
            <div className="section-header-meta">
              <span className="section-badge">{projects.length}</span>
              <button
                type="button"
                className="section-add-folder-btn"
                onClick={handleStartCreateProject}
                title="Create workspace folder"
                aria-label="Add folder"
              >
                <Plus size={11} />
              </button>
            </div>
          </div>

          {projects.length === 0 ? (
            <div className="empty-section-notice">
              No project folders yet. Click <strong>New Folder</strong> to organize debates.
            </div>
          ) : (
            projects.map((project) => {
              const isCollapsed = !!collapsedProjects[project.id];
              const projectDebates = activeConversations.filter((c) => c.project_id === project.id);
              const isEditing = editingProjectId === project.id;

              return (
                <div key={project.id} className="project-folder-group">
                  <div
                    className="project-folder-header"
                    onClick={() => toggleFolder(project.id)}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && toggleFolder(project.id)}
                  >
                    <span className="folder-chevron">
                      <Chevron open={!isCollapsed} size={13} />
                    </span>
                    <span className="folder-icon">
                      <Folder size={14} />
                    </span>

                    {isEditing ? (
                      <form className="inline-rename-form" onSubmit={(e) => handleSaveRenameProject(project.id, e)}>
                        <input
                          type="text"
                          className="rename-input"
                          value={editingProjectName}
                          onChange={(e) => setEditingProjectName(e.target.value)}
                          autoFocus
                          onClick={(e) => e.stopPropagation()}
                        />
                        <button type="submit" className="rename-save-btn" onClick={(e) => e.stopPropagation()}>
                          <Check size={12} />
                        </button>
                        <button
                          type="button"
                          className="rename-cancel-btn"
                          onClick={(e) => {
                            e.stopPropagation();
                            setEditingProjectId(null);
                          }}
                        >
                          <XMark size={12} />
                        </button>
                      </form>
                    ) : (
                      <span className="project-name" title={project.description || project.name}>
                        {project.name}
                      </span>
                    )}

                    <span className="project-count-badge">{projectDebates.length}</span>

                    <div className="project-header-actions" onClick={(e) => e.stopPropagation()}>
                      <button
                        type="button"
                        className="project-action-btn"
                        title="Start new debate in this project"
                        onClick={() => onNewConversation(project.id)}
                      >
                        <Plus size={12} />
                      </button>
                      <button
                        type="button"
                        className="project-action-btn"
                        title="Rename project"
                        onClick={(e) => handleStartRenameProject(project, e)}
                      >
                        <Pencil size={12} />
                      </button>
                      <button
                        type="button"
                        className="project-action-btn delete-action"
                        title="Delete project folder"
                        onClick={(e) => handleDeleteProjectClick(project, e)}
                      >
                        <Trash size={12} />
                      </button>
                    </div>
                  </div>

                  {!isCollapsed && (
                    <div className="project-debates-container">
                      {projectDebates.length === 0 ? (
                        <div className="project-empty-debates">
                          No debates in this folder.{' '}
                          <button
                            type="button"
                            className="inline-link-btn"
                            onClick={() => onNewConversation(project.id)}
                          >
                            + Start one
                          </button>
                        </div>
                      ) : (
                        projectDebates.map((conv) => renderConversationRow(conv, project.id))
                      )}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {/* Independent Debates Section */}
        <div className="sidebar-section">
          <div className="section-header">
            <span className="section-title">INDEPENDENT DEBATES</span>
            <span className="section-badge">{independentConversations.length}</span>
          </div>

          {independentConversations.length === 0 ? (
            <div className="empty-section-notice">No standalone debates</div>
          ) : (
            independentConversations.map((conv) => renderConversationRow(conv, null))
          )}
        </div>

        {/* Archived Debates Section */}
        {archivedConversations.length > 0 && (
          <div className="sidebar-section archived-section">
            <div
              className="section-header clickable-section-header"
              onClick={() => setShowArchived((prev) => !prev)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setShowArchived((prev) => !prev)}
            >
              <span className="section-title">
                <Archive size={12} className="section-icon" /> ARCHIVED DEBATES
              </span>
              <span className="section-badge">{archivedConversations.length}</span>
              <span className="section-chevron">
                <Chevron open={showArchived} size={12} />
              </span>
            </div>

            {showArchived && (
              <div className="archived-debates-list">
                {archivedConversations.map((conv) => renderConversationRow(conv, conv.project_id))}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        <div
          className={`opencode-status-pill ${isOk ? 'status-connected' : healthLoading ? 'status-connecting' : 'status-offline'}`}
          title={health?.diagnostics?.detail || (health?.opencode?.status || 'OpenCode Status')}
        >
          <span className="status-dot" />
          <span className="status-text">
            {healthLoading && !health
              ? 'Connecting to OpenCode…'
              : isOk
              ? `OpenCode :${health?.opencode?.port || 4097} (${health?.opencode?.models_count || 0} models)`
              : 'OpenCode Offline • BYOK Mode'}
          </span>
        </div>

        <button
          type="button"
          className="provider-keys-btn"
          onClick={() => setKeyModalOpen(true)}
        >
          <Key size={14} /> Provider API Keys
        </button>
      </div>

      <ProviderKeyModal
        isOpen={keyModalOpen}
        onClose={() => setKeyModalOpen(false)}
        onKeysUpdated={onKeysUpdated}
      />
    </div>
  );
}
