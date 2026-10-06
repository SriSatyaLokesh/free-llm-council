/**
 * Unified Vector SVG Icon Pack.
 *
 * Replaces all ad-hoc emojis and text glyphs across LLM Council with crisp,
 * scalable, theme-aware inline SVGs matching a 16x16 / 1.5-stroke design system.
 */

const base = {
  width: 16,
  height: 16,
  viewBox: '0 0 16 16',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.5,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  'aria-hidden': 'true',
  focusable: 'false',
};

export function Chevron({ open = false, size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d={open ? 'M4 6l4 4 4-4' : 'M6 4l4 4-4 4'} />
    </svg>
  );
}

export function Check({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M3.5 8.5l3 3 6-6" />
    </svg>
  );
}

export function Dot({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <circle cx="8" cy="8" r="2.5" />
    </svg>
  );
}

export function Folder({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M2 3.5h3.5l1.5 2H14v7.5a1 1 0 01-1 1H2a1 1 0 01-1-1v-8.5a1 1 0 011-1z" />
    </svg>
  );
}

export function FolderPlus({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M2 3.5h3.5l1.5 2H14v7.5a1 1 0 01-1 1H2a1 1 0 01-1-1v-8.5a1 1 0 011-1z" />
      <path d="M8 7.5v4M6 9.5h4" />
    </svg>
  );
}

export function FileText({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M3 2h7l3 3v8.5a1 1 0 01-1 1H3a1 1 0 01-1-1v-10.5a1 1 0 011-1z" />
      <path d="M10 2v3h3M5 7.5h6M5 10.5h4" />
    </svg>
  );
}

export function Archive({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <rect x="1.5" y="2.5" width="13" height="3" rx="0.75" />
      <path d="M2.5 5.5v7.5a1 1 0 001 1h9a1 1 0 001-1V5.5M6.5 8.5h3" />
    </svg>
  );
}

export function ArchiveRestore({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <rect x="1.5" y="2.5" width="13" height="3" rx="0.75" />
      <path d="M2.5 5.5v7.5a1 1 0 001 1h9a1 1 0 001-1V5.5M6 10l2-2 2 2M8 8v4" />
    </svg>
  );
}

export function Pencil({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M11.5 2.5l2 2-7.5 7.5H4v-2l7.5-7.5z" />
    </svg>
  );
}

export function Trash({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M2.5 4h11M5.5 4V2.5a.75.75 0 01.75-.75h3.5a.75.75 0 01.75.75V4M4 4l.75 9.5a1 1 0 001 .9h4.5a1 1 0 001-.9L12 4M6.5 7v4.5M9.5 7v4.5" />
    </svg>
  );
}

export function Copy({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <rect x="5" y="5" width="8.5" height="8.5" rx="1" />
      <path d="M3.5 11H2.5a1 1 0 01-1-1V2.5a1 1 0 011-1H10a1 1 0 011 1V3.5" />
    </svg>
  );
}

export function Package({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M8 1.5l6 3.5v6l-6 3.5-6-3.5v-6l6-3.5z" />
      <path d="M8 8.5L2 5M8 8.5l6-3.5M8 8.5v6.5" />
    </svg>
  );
}

export function Move({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M1.5 8h13M11 4.5l3.5 3.5-3.5 3.5M5 11.5L1.5 8 5 4.5" />
    </svg>
  );
}

export function Key({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <circle cx="5" cy="8" r="3.25" />
      <path d="M8.25 8h6M11.5 8v2M13.5 8v1.5" />
    </svg>
  );
}

export function Target({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <circle cx="8" cy="8" r="6" />
      <circle cx="8" cy="8" r="2.5" />
      <path d="M8 1v2M8 13v2M1 8h2M13 8h2" />
    </svg>
  );
}

export function Zap({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M8.5 1.5L2.5 9h5l-1 5.5 6-7.5h-5l1-5.5z" />
    </svg>
  );
}

export function AlertTriangle({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M8 2l6.5 11.5H1.5L8 2zM8 6.5v3M8 11.5v.5" />
    </svg>
  );
}

export function Plus({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M8 3v10M3 8h10" />
    </svg>
  );
}

export function XMark({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M3.5 3.5l9 9M12.5 3.5l-9 9" />
    </svg>
  );
}
