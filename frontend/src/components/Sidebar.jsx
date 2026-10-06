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
  MoreHorizontal,
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
  onDeleteConversation,
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

  // Conversation UI state (Rename, Dropdown options, Drag-and-Drop, Archive)
  const [editingConvId, setEditingConvId] = useState(null);
  const [editingConvTitle, setEditingConvTitle] = useState('');
  const [activeOptionsDropdownConvId, setActiveOptionsDropdownConvId] = useState(null);
  const [draggingConvId, setDraggingConvId] = useState(null);
  const [dragOverTarget, setDragOverTarget] = useState(null);
  const [copiedConvId, setCopiedConvId] = useState(null);
  const [showArchived, setShowArchived] = useState(false);

  // Dismiss dropdown on outside clicks or Escape key
  useEffect(() => {
    const handleGlobalClick = () => {
      setActiveOptionsDropdownConvId(null);
    };
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setActiveOptionsDropdownConvId(null);
        setEditingConvId(null);
      }
    };
    document.addEventListener('click', handleGlobalClick);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('click', handleGlobalClick);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

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

  const handleStartRenameConv = (conv, e) => {
    e.stopPropagation();
    setActiveOptionsDropdownConvId(null);
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
    setActiveOptionsDropdownConvId(null);
    if (!isCurrentlyArchived) {
      // Ensure user sees the debate transition to the archived folder
      setShowArchived(true);
    }
    if (onArchiveConversation) {
      await onArchiveConversation(convId, !isCurrentlyArchived);
    }
  };

  const handleDeleteConv = async (conv, e) => {
    e.stopPropagation();
    setActiveOptionsDropdownConvId(null);
    const confirmMsg = `Delete debate "${conv.title || 'New Debate'}"?\nThis deliberation will be permanently deleted.`;
    if (window.confirm(confirmMsg) && onDeleteConversation) {
      await onDeleteConversation(conv.id);
    }
  };

  // Drag and drop handlers
  const handleDragStart = (e, conv) => {
    e.dataTransfer.setData('text/plain', conv.id);
    e.dataTransfer.effectAllowed = 'move';
    setDraggingConvId(conv.id);
  };

  const handleDragEnd = () => {
    setDraggingConvId(null);
    setDragOverTarget(null);
  };

  const handleFolderDragOver = (e, projectId) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    if (dragOverTarget !== projectId) {
      setDragOverTarget(projectId);
    }
  };

  const handleFolderDragLeave = (e, projectId) => {
    if (e.currentTarget.contains(e.relatedTarget)) return;
    if (dragOverTarget === projectId) {
      setDragOverTarget(null);
    }
  };

  const handleFolderDrop = async (e, projectId) => {
    e.preventDefault();
    e.stopPropagation();
    const convId = e.dataTransfer.getData('text/plain') || draggingConvId;
    setDragOverTarget(null);
    setDraggingConvId(null);
    if (convId && onMoveConversation) {
      await onMoveConversation(convId, projectId);
    }
  };

  const handleIndependentDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    if (dragOverTarget !== 'independent') {
      setDragOverTarget('independent');
    }
  };

  const handleIndependentDragLeave = (e) => {
    if (e.currentTarget.contains(e.relatedTarget)) return;
    if (dragOverTarget === 'independent') {
      setDragOverTarget(null);
    }
  };

  const handleIndependentDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    const convId = e.dataTransfer.getData('text/plain') || draggingConvId;
    setDragOverTarget(null);
    setDraggingConvId(null);
    if (convId && onMoveConversation) {
      await onMoveConversation(convId, null);
    }
  };

  // Partition active vs archived
  const activeConversations = conversations.filter((c) => !c.archived);
  const archivedConversations = conversations.filter((c) => !!c.archived);
  const independentConversations = activeConversations.filter((c) => !c.project_id);

  // Render helper for single conversation row
  const renderConversationRow = (conv, currentFolderId = null) => {
    const isEditing = editingConvId === conv.id;
    const isDropdownOpen = activeOptionsDropdownConvId === conv.id;
    const isDragging = draggingConvId === conv.id;

    return (
      <div
        key={conv.id}
        draggable={!isEditing}
        onDragStart={(e) => handleDragStart(e, conv)}
        onDragEnd={handleDragEnd}
        className={`conversation-row ${conv.id === currentConversationId ? 'active' : ''} ${conv.archived ? 'archived-row' : ''} ${isDragging ? 'is-dragging' : ''}`}
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
            title={`${conv.title || 'New Debate'}\n(Drag into folders to organize)`}
          >
            <span className="conversation-title">{conv.title || 'New Debate'}</span>
            <span className="conversation-meta">
              {conv.message_count} msg{conv.message_count === 1 ? '' : 's'}
              {conv.archived && <span className="archived-meta-badge">archived</span>}
            </span>
          </button>
        )}

        <div className="conv-actions-group" onClick={(e) => e.stopPropagation()}>
          {/* Quick Action 1: Copy ID */}
          <button
            type="button"
            className="conv-icon-btn"
            title={`Copy ID (${conv.id})`}
            onClick={(e) => handleCopyConvId(conv.id, e)}
          >
            {copiedConvId === conv.id ? <Check size={12} /> : <Copy size={12} />}
          </button>

          {/* Quick Action 2: Export Deliberation ZIP */}
          <a
            href={api.getZipExportUrl(conv.id)}
            download
            className="conv-icon-btn"
            title="Download deliberation as ZIP"
            onClick={(e) => e.stopPropagation()}
          >
            <Package size={12} />
          </a>

          {/* Three Dots Options Menu Dropdown */}
          <div className="conv-options-container">
            <button
              type="button"
              className={`conv-icon-btn conv-options-btn ${isDropdownOpen ? 'active' : ''}`}
              title="More debate options"
              onClick={(e) => {
                e.stopPropagation();
                setActiveOptionsDropdownConvId(isDropdownOpen ? null : conv.id);
              }}
              aria-expanded={isDropdownOpen}
            >
              <MoreHorizontal size={13} />
            </button>

            {isDropdownOpen && (
              <div
                className="conv-options-dropdown"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  type="button"
                  className="conv-dropdown-item"
                  onClick={(e) => handleStartRenameConv(conv, e)}
                >
                  <Pencil size={12} />
                  <span>Rename Debate</span>
                </button>

                <button
                  type="button"
                  className="conv-dropdown-item"
                  onClick={(e) => handleToggleArchiveConv(conv.id, conv.archived, e)}
                >
                  {conv.archived ? <ArchiveRestore size={12} /> : <Archive size={12} />}
                  <span>{conv.archived ? 'Restore Debate' : 'Archive Debate'}</span>
                </button>

                <div className="conv-dropdown-divider" />

                <button
                  type="button"
                  className="conv-dropdown-item danger-item"
                  onClick={(e) => handleDeleteConv(conv, e)}
                >
                  <Trash size={12} />
                  <span>Delete Debate</span>
                </button>
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
                    className={`project-folder-header ${dragOverTarget === project.id ? 'drag-over' : ''}`}
                    onClick={() => toggleFolder(project.id)}
                    onDragOver={(e) => handleFolderDragOver(e, project.id)}
                    onDragLeave={(e) => handleFolderDragLeave(e, project.id)}
                    onDrop={(e) => handleFolderDrop(e, project.id)}
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

        {/* Independent Debates Section (Droppable to detach debate from folders) */}
        <div
          className={`sidebar-section independent-section ${dragOverTarget === 'independent' ? 'drag-over' : ''}`}
          onDragOver={handleIndependentDragOver}
          onDragLeave={handleIndependentDragLeave}
          onDrop={handleIndependentDrop}
        >
          <div className="section-header">
            <span className="section-title">INDEPENDENT DEBATES</span>
            <span className="section-badge">{independentConversations.length}</span>
          </div>

          {independentConversations.length === 0 ? (
            <div className="empty-section-notice">
              {dragOverTarget === 'independent' ? 'Drop here to make standalone' : 'No standalone debates'}
            </div>
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
