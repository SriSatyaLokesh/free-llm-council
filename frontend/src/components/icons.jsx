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

export function ChevronDown({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M4 6l4 4 4-4" />
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

export function MoreVertical({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className} stroke="none" fill="currentColor">
      <circle cx="8" cy="3" r="1.3" />
      <circle cx="8" cy="8" r="1.3" />
      <circle cx="8" cy="13" r="1.3" />
    </svg>
  );
}

export function MoreHorizontal({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className} stroke="none" fill="currentColor">
      <circle cx="3" cy="8" r="1.3" />
      <circle cx="8" cy="8" r="1.3" />
      <circle cx="13" cy="8" r="1.3" />
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

export function GroupAILogo({ size = 20, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      className={className}
      aria-hidden="true"
      focusable="false"
    >
      <defs>
        <linearGradient id="logo-bg" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#1E293B" />
          <stop offset="100%" stopColor="#0B0D14" />
        </linearGradient>
        <linearGradient id="logo-blue" x1="16" y1="4" x2="16" y2="12" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#60A5FA" />
          <stop offset="100%" stopColor="#2563EB" />
        </linearGradient>
        <linearGradient id="logo-purple" x1="5" y1="18" x2="12" y2="26" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#C084FC" />
          <stop offset="100%" stopColor="#7C3AED" />
        </linearGradient>
        <linearGradient id="logo-emerald" x1="20" y1="18" x2="27" y2="26" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#34D399" />
          <stop offset="100%" stopColor="#059669" />
        </linearGradient>
        <linearGradient id="logo-spark" x1="13" y1="13" x2="19" y2="19" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#FFFFFF" />
          <stop offset="50%" stopColor="#38BDF8" />
          <stop offset="100%" stopColor="#0284C7" />
        </linearGradient>
      </defs>

      <rect width="32" height="32" rx="7.5" fill="url(#logo-bg)" stroke="rgba(255,255,255,0.15)" strokeWidth="1" />
      <path d="M16 8 C11 12 8 17 8 22" stroke="#3B82F6" strokeWidth="1.2" strokeLinecap="round" strokeDasharray="1 2" opacity="0.65" />
      <path d="M16 8 C21 12 24 17 24 22" stroke="#10B981" strokeWidth="1.2" strokeLinecap="round" strokeDasharray="1 2" opacity="0.65" />
      <path d="M8 22 C13 23.5 19 23.5 24 22" stroke="#8B5CF6" strokeWidth="1.2" strokeLinecap="round" strokeDasharray="1 2" opacity="0.65" />

      <line x1="16" y1="8" x2="16" y2="15.5" stroke="#60A5FA" strokeWidth="1" strokeLinecap="round" opacity="0.75" />
      <line x1="8" y1="22" x2="16" y2="15.5" stroke="#C084FC" strokeWidth="1" strokeLinecap="round" opacity="0.75" />
      <line x1="24" y1="22" x2="16" y2="15.5" stroke="#34D399" strokeWidth="1" strokeLinecap="round" opacity="0.75" />

      <circle cx="16" cy="8" r="3.2" fill="url(#logo-blue)" />
      <circle cx="16" cy="8" r="1.2" fill="#FFFFFF" />

      <circle cx="8" cy="22" r="3.2" fill="url(#logo-purple)" />
      <circle cx="8" cy="22" r="1.2" fill="#FFFFFF" />

      <circle cx="24" cy="22" r="3.2" fill="url(#logo-emerald)" />
      <circle cx="24" cy="22" r="1.2" fill="#FFFFFF" />

      <path d="M16 12 C16 14.3 14.3 15.5 12.5 15.5 C14.3 15.5 16 16.7 16 19 C16 16.7 17.7 15.5 19.5 15.5 C17.7 15.5 16 14.3 16 12 Z" fill="url(#logo-spark)" />
    </svg>
  );
}

export function Printer({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M4 5.5V2h8v3.5M4 11H2.5a1.5 1.5 0 01-1.5-1.5v-3A1.5 1.5 0 012.5 5h11A1.5 1.5 0 0115 6.5v3a1.5 1.5 0 01-1.5 1.5H12M4 9h8v5H4V9z" />
    </svg>
  );
}

export function Download({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M2.5 11.5v2a1 1 0 001 1h9a1 1 0 001-1v-2M8 2v7.5M5 6.5l3 3 3-3" />
    </svg>
  );
}

export function Eye({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M1.5 8s2.5-4.5 6.5-4.5 6.5 4.5 6.5 4.5-2.5 4.5-6.5 4.5-6.5-4.5-6.5-4.5z" />
      <circle cx="8" cy="8" r="2" />
    </svg>
  );
}

export function Code({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M5.5 5L2.5 8l3 3M10.5 5l3 3-3 3" />
    </svg>
  );
}

export function TableIcon({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <rect x="2" y="2.5" width="12" height="11" rx="1.5" />
      <path d="M2 6.5h12M7 6.5v7" />
    </svg>
  );
}

export function BarChart({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M2.5 13.5h11M5 11v-4M8 11v-7M11 11v-5" />
    </svg>
  );
}

export function LinkIcon({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M6.5 9.5a3.5 3.5 0 005 0l2-2a3.5 3.5 0 00-5-5l-1 1M9.5 6.5a3.5 3.5 0 00-5 0l-2 2a3.5 3.5 0 005 5l1-1M5.5 10.5l5-5" />
    </svg>
  );
}

export function ShareIcon({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <circle cx="12" cy="3.5" r="2" />
      <circle cx="4" cy="8" r="2" />
      <circle cx="12" cy="12.5" r="2" />
      <path d="M5.8 9l4.4 2.5M10.2 4.5L5.8 7" />
    </svg>
  );
}

export function UsersIcon({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M11 13.5v-1a2.5 2.5 0 00-2.5-2.5h-5A2.5 2.5 0 001 12.5v1" />
      <circle cx="6" cy="5" r="2.5" />
      <path d="M15 13.5v-1a2.5 2.5 0 00-2-2.45M11.5 2.6a2.5 2.5 0 010 4.8" />
    </svg>
  );
}

export function SlidersIcon({ size = 16, className = '' }) {
  return (
    <svg {...base} width={size} height={size} className={className}>
      <path d="M3 13.5v-4M3 6.5V2.5M1 6.5h4M8 13.5V9.5M8 6.5V2.5M6 9.5h4M13 13.5v-2M13 8.5V2.5M11 11.5h4" />
    </svg>
  );
}


