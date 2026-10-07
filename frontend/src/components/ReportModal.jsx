import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  FileText,
  TableIcon,
  Copy,
  Check,
  Printer,
  Download,
  Package,
  Eye,
  Code,
  XMark,
  Zap,
} from './icons';
import { api } from '../api';
import './ReportModal.css';

/**
 * Industry-Standard Deliberation Report Modal.
 *
 * Provides dual-report switching (Executive Brief vs Deep-Dive Technical Matrix),
 * interactive rendered preview, raw markdown inspection, one-click copy,
 * direct .md and .zip downloads, and print/PDF optimization.
 */
export default function ReportModal({ conversation, isOpen, onClose }) {
  const [reportType, setReportType] = useState('executive'); // 'executive' | 'detailed'
  const [viewMode, setViewMode] = useState('preview'); // 'preview' | 'raw'
  const [reportsData, setReportsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [idCopied, setIdCopied] = useState(false);

  useEffect(() => {
    if (!isOpen || !conversation?.id) return;

    let isMounted = true;
    setLoading(true);
    setError(null);

    api
      .getReports(conversation.id)
      .then((data) => {
        if (isMounted) {
          setReportsData(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          console.error('Failed to load reports:', err);
          setError(err.message || 'Unable to generate deliberation reports.');
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [isOpen, conversation?.id]);

  // Handle ESC key to close
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const currentMarkdown =
    reportType === 'detailed'
      ? reportsData?.detailed_report || ''
      : reportsData?.executive_report || '';

  // Extract metadata stats from conversation assistant verdict if available
  let chairman = 'Designated Chairman';
  let membersCount = 0;
  let totalTokens = 0;
  let confidence = 'High';

  if (conversation?.messages) {
    for (const msg of conversation.messages) {
      if (msg.role === 'assistant' && msg.council) {
        const c = msg.council;
        const meta = c.metadata || {};
        const verdict = c.verdict || {};
        chairman = verdict.model || meta.chairman || chairman;
        membersCount = meta.members?.length || c.positions?.length || membersCount;
        totalTokens = meta.total_tokens || totalTokens;
        if (verdict.sections?.confidence) {
          confidence = verdict.sections.confidence;
        }
        break;
      }
    }
  }

  const handleCopyMarkdown = async () => {
    if (!currentMarkdown) return;
    try {
      await navigator.clipboard.writeText(currentMarkdown);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy markdown:', err);
    }
  };

  const handleCopyId = async () => {
    if (!conversation?.id) return;
    try {
      await navigator.clipboard.writeText(conversation.id);
      setIdCopied(true);
      setTimeout(() => setIdCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy ID:', err);
    }
  };

  const handleDownloadMd = () => {
    if (!conversation?.id) return;
    const formatParam = reportType === 'detailed' ? 'detailed' : 'executive';
    window.open(api.getReportExportUrl(conversation.id, formatParam), '_blank');
  };

  const handleDownloadZip = () => {
    if (!conversation?.id) return;
    window.open(api.getZipExportUrl(conversation.id), '_blank');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="report-modal-backdrop" onClick={onClose} role="dialog" aria-modal="true">
      <div className="report-modal-dialog" onClick={(e) => e.stopPropagation()}>
        {/* Navigation & Toolbar Header */}
        <header className="report-modal-header">
          <div className="report-header-left">
            <div className="report-title-row">
              <span className="report-header-badge">
                <FileText size={14} />
                Deliberation Report
              </span>
              <button
                type="button"
                className="report-id-pill"
                onClick={handleCopyId}
                title={`Deliberation ID: ${conversation.id}\nClick to copy full ID`}
              >
                <span className="report-id-text">
                  ID: {conversation?.id ? conversation.id.slice(0, 8) : 'unknown'}…
                </span>
                {idCopied ? <Check size={11} className="id-copied-icon" /> : <Copy size={11} />}
              </button>
            </div>
            <h2 className="report-dialog-title">
              {conversation?.title || 'Council Strategic Deliberation'}
            </h2>
          </div>

          {/* Central Dual-Mode Switcher */}
          <div className="report-mode-switcher" role="tablist" aria-label="Report Format Selector">
            <button
              type="button"
              role="tab"
              aria-selected={reportType === 'executive'}
              className={`report-tab-btn ${reportType === 'executive' ? 'active' : ''}`}
              onClick={() => setReportType('executive')}
            >
              <Zap size={14} />
              <span>Executive Brief</span>
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={reportType === 'detailed'}
              className={`report-tab-btn ${reportType === 'detailed' ? 'active' : ''}`}
              onClick={() => setReportType('detailed')}
            >
              <TableIcon size={14} />
              <span>Deep-Dive Matrix</span>
            </button>
          </div>

          {/* Right Action Tools */}
          <div className="report-header-actions">
            {/* View Mode Toggle */}
            <div className="report-view-toggle">
              <button
                type="button"
                className={`view-toggle-btn ${viewMode === 'preview' ? 'active' : ''}`}
                onClick={() => setViewMode('preview')}
                title="Rendered publication preview"
              >
                <Eye size={13} />
                <span>Preview</span>
              </button>
              <button
                type="button"
                className={`view-toggle-btn ${viewMode === 'raw' ? 'active' : ''}`}
                onClick={() => setViewMode('raw')}
                title="View raw Markdown syntax"
              >
                <Code size={13} />
                <span>Raw</span>
              </button>
            </div>

            <button
              type="button"
              className="report-tool-btn"
              onClick={handleCopyMarkdown}
              title="Copy formatted markdown to clipboard"
            >
              {copied ? <Check size={14} className="tool-success" /> : <Copy size={14} />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>

            <button
              type="button"
              className="report-tool-btn"
              onClick={handlePrint}
              title="Print or export as publication-grade PDF"
            >
              <Printer size={14} />
              <span>Print / PDF</span>
            </button>

            <button
              type="button"
              className="report-tool-btn report-primary-tool"
              onClick={handleDownloadMd}
              title={`Download active ${reportType} report as Markdown`}
            >
              <Download size={14} />
              <span>Download .MD</span>
            </button>

            <button
              type="button"
              className="report-tool-btn"
              onClick={handleDownloadZip}
              title="Download full deliberation bundle ZIP (both reports + raw data)"
            >
              <Package size={14} />
              <span>ZIP</span>
            </button>

            <button
              type="button"
              className="report-close-btn"
              onClick={onClose}
              title="Close report modal (Esc)"
              aria-label="Close report modal"
            >
              <XMark size={16} />
            </button>
          </div>
        </header>

        {/* Telemetry KPI Strip */}
        <div className="report-kpi-strip">
          <div className="report-kpi-item">
            <span className="kpi-label">Chairman Synthesis</span>
            <span className="kpi-value kpi-mono">{chairman}</span>
          </div>
          <div className="report-kpi-item">
            <span className="kpi-label">Council Roster</span>
            <span className="kpi-value">{membersCount > 0 ? `${membersCount} Models` : 'Synthesized'}</span>
          </div>
          <div className="report-kpi-item">
            <span className="kpi-label">Confidence Assessment</span>
            <span className="kpi-value kpi-confidence">{confidence}</span>
          </div>
          <div className="report-kpi-item">
            <span className="kpi-label">Compute Footprint</span>
            <span className="kpi-value">{totalTokens > 0 ? `${totalTokens.toLocaleString()} tokens` : 'Recorded'}</span>
          </div>
          <div className="report-kpi-item report-kpi-type">
            <span className="kpi-label">Active Format</span>
            <span className="kpi-value kpi-type-tag">
              {reportType === 'detailed' ? 'Comparative Matrix & Audit' : 'Executive Briefing'}
            </span>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="report-modal-body">
          {loading ? (
            <div className="report-loading-state">
              <div className="report-spinner" aria-hidden="true" />
              <p>Synthesizing deliberation report & comparative matrix…</p>
            </div>
          ) : error ? (
            <div className="report-error-state">
              <p className="error-title">Unable to generate report</p>
              <p className="error-detail">{error}</p>
            </div>
          ) : !currentMarkdown ? (
            <div className="report-empty-state">
              <p>No council deliberation records found for this debate.</p>
            </div>
          ) : viewMode === 'raw' ? (
            <div className="report-raw-container">
              <textarea
                readOnly
                className="report-raw-textarea"
                value={currentMarkdown}
                aria-label="Raw Markdown source"
              />
            </div>
          ) : (
            <div className="report-preview-container markdown-content">
              <ReactMarkdown>{currentMarkdown}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
