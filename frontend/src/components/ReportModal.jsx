import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  FileText,
  TableIcon,
  Copy,
  Check,
  Download,
  Package,
  Eye,
  Code,
  XMark,
  Zap,
  LinkIcon,
  ChevronDown,
  ShareIcon,
  Printer,
} from './icons';
import { api } from '../api';
import { getShareableUrl } from '../utils/url';
import './ReportModal.css';

/**
 * Industry-Standard Deliberation Report Modal.
 *
 * Provides dual-report switching (Executive Brief vs Deep-Dive Technical Matrix),
 * interactive rendered preview, raw markdown inspection, one-click copy,
 * direct .pdf, .md, and .zip downloads, and isolated print/PDF optimization.
 */
export default function ReportModal({
  conversation,
  isOpen,
  reportType: controlledReportType,
  onReportTypeChange,
  onClose,
}) {
  const [internalReportType, setInternalReportType] = useState('executive');
  const reportType = controlledReportType || internalReportType;
  const [viewMode, setViewMode] = useState('preview'); // 'preview' | 'raw'
  const [reportsData, setReportsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [idCopied, setIdCopied] = useState(false);
  const [reportLinkCopied, setReportLinkCopied] = useState(false);
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [isShareDropdownOpen, setIsShareDropdownOpen] = useState(false);
  const shareDropdownRef = useRef(null);
  const previewRef = useRef(null);

  // Close dropdown on outside click or Escape key
  useEffect(() => {
    if (!isShareDropdownOpen) return;
    const handleClickOutside = (e) => {
      if (shareDropdownRef.current && !shareDropdownRef.current.contains(e.target)) {
        setIsShareDropdownOpen(false);
      }
    };
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setIsShareDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isShareDropdownOpen]);

  const handleSelectReportType = (type) => {
    setInternalReportType(type);
    if (onReportTypeChange) {
      onReportTypeChange(type);
    }
  };

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
      console.error('Failed to copy debate ID:', err);
    }
  };

  const handleCopyReportLink = async () => {
    if (!conversation?.id) return;
    const shareUrl = getShareableUrl(conversation.id, reportType);
    try {
      await navigator.clipboard.writeText(shareUrl);
      setReportLinkCopied(true);
      setTimeout(() => setReportLinkCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy report link:', err);
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

  const handlePrintIsolated = () => {
    const cleanFileName = `council-${reportType}-report-${conversation?.id ? conversation.id.slice(0, 8) : 'export'}`;
    const contentHtml = previewRef.current ? previewRef.current.innerHTML : '';

    const iframe = document.createElement('iframe');
    iframe.style.position = 'fixed';
    iframe.style.right = '0';
    iframe.style.bottom = '0';
    iframe.style.width = '0';
    iframe.style.height = '0';
    iframe.style.border = '0';
    document.body.appendChild(iframe);

    const doc = iframe.contentWindow.document;
    doc.open();
    doc.write(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>${cleanFileName}</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 16mm 16mm 18mm 16mm;
    }
    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.55;
      color: #0f172a;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }
    .print-header-banner {
      border-bottom: 2px solid #0f172a;
      padding-bottom: 12px;
      margin-bottom: 16px;
    }
    .print-badge {
      display: inline-block;
      font-size: 7.5pt;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: #0f172a;
      color: #ffffff;
      padding: 3px 8px;
      border-radius: 3px;
      margin-bottom: 8px;
    }
    .print-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin: 0 0 4px 0;
      color: #0f172a;
    }
    .print-subtitle {
      font-size: 0.9rem;
      color: #475569;
      margin: 0;
    }
    .print-meta-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 10px 12px;
      margin-bottom: 20px;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    .print-meta-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .print-meta-label {
      font-size: 7.5pt;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #64748b;
      font-weight: 600;
    }
    .print-meta-value {
      font-size: 9pt;
      font-weight: 600;
      color: #0f172a;
    }
    h1, h2, h3, h4 {
      color: #0f172a;
      page-break-after: avoid;
      break-after: avoid;
    }
    h1 {
      font-size: 1.4rem;
      border-bottom: 1.5px solid #cbd5e1;
      padding-bottom: 4px;
      margin-top: 20px;
      margin-bottom: 10px;
    }
    h2 {
      font-size: 1.18rem;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 4px;
      margin-top: 18px;
      margin-bottom: 8px;
    }
    h3 {
      font-size: 1.05rem;
      margin-top: 14px;
      margin-bottom: 6px;
    }
    p, ul, ol {
      margin: 0.45rem 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
      font-size: 9pt;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    th {
      background: #1e293b !important;
      color: #ffffff !important;
      font-weight: 600;
      text-align: left;
      padding: 8px 10px;
      border: 1px solid #1e293b;
    }
    td {
      padding: 7px 10px;
      border: 1px solid #cbd5e1;
      vertical-align: top;
      color: #334155;
    }
    tr:nth-child(even) td {
      background: #f8fafc !important;
    }
    pre {
      background: #f1f5f9 !important;
      border: 1px solid #cbd5e1 !important;
      border-radius: 4px;
      padding: 10px 12px;
      font-family: "Cascadia Code", Consolas, Monaco, "Courier New", monospace;
      font-size: 8pt;
      line-height: 1.35;
      white-space: pre;
      overflow-x: auto;
      page-break-inside: avoid;
      break-inside: avoid;
      margin: 12px 0;
    }
    code {
      font-family: "Cascadia Code", Consolas, Monaco, "Courier New", monospace;
      font-size: 0.9em;
      background: #f1f5f9;
      padding: 2px 4px;
      border-radius: 3px;
    }
    pre code {
      background: transparent;
      padding: 0;
      border: none;
    }
    blockquote {
      border-left: 4px solid #3b82f6;
      background: #eff6ff;
      margin: 10px 0;
      padding: 8px 12px;
      color: #1e3a8a;
      border-radius: 0 4px 4px 0;
    }
    hr {
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 16px 0;
    }
  </style>
</head>
<body>
  <div class="print-header-banner">
    <div class="print-badge">Free LLM Council Deliberation Report</div>
    <h1 class="print-title">${conversation?.title || 'Council Deliberation'}</h1>
    <p class="print-subtitle">${reportType === 'detailed' ? 'Comprehensive Deep-Dive Technical Matrix' : 'Executive Summary Brief'}</p>
  </div>
  <div class="print-meta-grid">
    <div class="print-meta-item">
      <span class="print-meta-label">Deliberation ID</span>
      <span class="print-meta-value">${conversation?.id ? conversation.id.slice(0, 8) + '...' : 'N/A'}</span>
    </div>
    <div class="print-meta-item">
      <span class="print-meta-label">Chairman</span>
      <span class="print-meta-value">${chairman}</span>
    </div>
    <div class="print-meta-item">
      <span class="print-meta-label">Council Size</span>
      <span class="print-meta-value">${membersCount} Models</span>
    </div>
    <div class="print-meta-item">
      <span class="print-meta-label">Confidence</span>
      <span class="print-meta-value">${confidence}</span>
    </div>
    <div class="print-meta-item">
      <span class="print-meta-label">Tokens</span>
      <span class="print-meta-value">${totalTokens ? totalTokens.toLocaleString() : 'N/A'}</span>
    </div>
    <div class="print-meta-item">
      <span class="print-meta-label">Format</span>
      <span class="print-meta-value">${reportType === 'detailed' ? 'Technical Matrix' : 'Executive Brief'}</span>
    </div>
  </div>
  ${contentHtml}
</body>
</html>`);
    doc.close();

    iframe.contentWindow.focus();
    setTimeout(() => {
      iframe.contentWindow.print();
      setTimeout(() => {
        document.body.removeChild(iframe);
      }, 2500);
    }, 250);
  };

  const handleDownloadPdf = async () => {
    if (!conversation?.id) return;
    const formatParam = reportType === 'detailed' ? 'detailed' : 'executive';
    const pdfUrl = api.getPdfExportUrl(conversation.id, formatParam);

    setDownloadingPdf(true);
    try {
      const res = await fetch(pdfUrl);
      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const fmtTag = formatParam === 'detailed' ? 'detailed' : 'executive';
        a.download = `council-${fmtTag}-report-${conversation.id.slice(0, 8)}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        handlePrintIsolated();
      }
    } catch (err) {
      console.warn('Backend PDF download error, falling back to print-to-PDF:', err);
      handlePrintIsolated();
    } finally {
      setDownloadingPdf(false);
    }
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
                title={`Debate ID: ${conversation?.id || 'unknown'}\nClick to copy debate ID`}
              >
                {idCopied ? (
                  <>
                    <Check size={12} className="id-copied-icon" />
                    <span className="report-copied-tag">Debate ID Copied</span>
                  </>
                ) : (
                  <>
                    <Copy size={12} />
                    <span>Copy Debate ID</span>
                  </>
                )}
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
              onClick={() => handleSelectReportType('executive')}
            >
              <Zap size={14} />
              <span>Executive Brief</span>
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={reportType === 'detailed'}
              className={`report-tab-btn ${reportType === 'detailed' ? 'active' : ''}`}
              onClick={() => handleSelectReportType('detailed')}
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

            {/* Share Report Dropdown */}
            <div className="report-share-dropdown-wrapper" ref={shareDropdownRef}>
              <button
                type="button"
                className={`report-tool-btn report-share-dropdown-btn ${isShareDropdownOpen ? 'active' : ''}`}
                onClick={() => setIsShareDropdownOpen((v) => !v)}
                title="Share report URL or export as PDF, Markdown, or ZIP"
                aria-haspopup="true"
                aria-expanded={isShareDropdownOpen}
              >
                <ShareIcon size={14} />
                <span>Share Report</span>
                <ChevronDown size={13} className={`dropdown-caret ${isShareDropdownOpen ? 'open' : ''}`} />
              </button>

              {isShareDropdownOpen && (
                <div className="report-share-dropdown-menu" role="menu">
                  <button
                    type="button"
                    className="report-share-dropdown-item"
                    onClick={handleCopyReportLink}
                    role="menuitem"
                    title="Copy shareable report link to clipboard"
                  >
                    <span className="share-item-icon">
                      {reportLinkCopied ? <Check size={14} className="copied-icon" /> : <LinkIcon size={14} />}
                    </span>
                    <div className="share-item-text">
                      <span className="share-item-label">
                        {reportLinkCopied ? 'Link Copied to Clipboard!' : 'Copy Link'}
                      </span>
                      <span className="share-item-hint">Shareable direct report URL</span>
                    </div>
                  </button>

                  <div className="report-share-dropdown-divider" />

                  <button
                    type="button"
                    className="report-share-dropdown-item"
                    onClick={() => {
                      handleDownloadPdf();
                      setIsShareDropdownOpen(false);
                    }}
                    disabled={downloadingPdf}
                    role="menuitem"
                    title="Download publication-grade deliberation PDF"
                  >
                    <span className="share-item-icon">
                      <Printer size={14} />
                    </span>
                    <div className="share-item-text">
                      <span className="share-item-label">
                        {downloadingPdf ? 'Exporting PDF…' : 'Download PDF'}
                      </span>
                      <span className="share-item-hint">Publication-grade styled report</span>
                    </div>
                  </button>

                  <button
                    type="button"
                    className="report-share-dropdown-item"
                    onClick={() => {
                      handleDownloadMd();
                      setIsShareDropdownOpen(false);
                    }}
                    role="menuitem"
                    title="Download Markdown (.md) report transcript"
                  >
                    <span className="share-item-icon">
                      <FileText size={14} />
                    </span>
                    <div className="share-item-text">
                      <span className="share-item-label">Download Markdown</span>
                      <span className="share-item-hint">Raw Markdown document (.md)</span>
                    </div>
                  </button>

                  <button
                    type="button"
                    className="report-share-dropdown-item"
                    onClick={() => {
                      handleDownloadZip();
                      setIsShareDropdownOpen(false);
                    }}
                    role="menuitem"
                    title="Download full deliberation bundle ZIP"
                  >
                    <span className="share-item-icon">
                      <Package size={14} />
                    </span>
                    <div className="share-item-text">
                      <span className="share-item-label">Download ZIP</span>
                      <span className="share-item-hint">Full package: reports, json & summary</span>
                    </div>
                  </button>
                </div>
              )}
            </div>

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
              <div className="report-raw-toolbar">
                <span className="raw-toolbar-info">
                  Raw Markdown ({reportType === 'detailed' ? 'Deep-Dive Matrix' : 'Executive Brief'})
                </span>
                <button
                  type="button"
                  className="report-tool-btn raw-copy-btn"
                  onClick={handleCopyMarkdown}
                  title="Copy raw Markdown syntax to clipboard"
                >
                  {copied ? <Check size={14} className="tool-success" /> : <Copy size={14} />}
                  <span>{copied ? 'Copied' : 'Copy Raw Markdown'}</span>
                </button>
              </div>
              <textarea
                readOnly
                className="report-raw-textarea"
                value={currentMarkdown}
                aria-label="Raw Markdown source"
              />
            </div>
          ) : (
            <div ref={previewRef} className="report-preview-container markdown-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  table: ({ node, ...props }) => (
                    <div className="report-table-scroll">
                      <table {...props} />
                    </div>
                  ),
                }}
              >
                {currentMarkdown}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
