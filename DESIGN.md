# Design System: Taste Standard & Antigravity Chat Architecture

> **Aesthetic Foundation:** Antigravity 2.0 / Antigravity IDE Chat Interface & Anti-Slop Taste Skill (`design-taste-frontend`).
> **Goal:** High-utility, distraction-free AI workspace with instantaneous rendering, tactile interactions, zero layout shifts, and ergonomic handling.

---

## 1. Dials & Atmosphere

| Dial | Level (1–10) | Description |
|---|---|---|
| **Creativity** | `6` | Refined, focused software utility. Elevated beyond sterile enterprise forms, without gratuitous animations. |
| **Density** | `6` | Balanced developer density. Information-rich panels with comfortable padding and clear optical hierarchy. |
| **Variance** | `5` | Consistent structural alignment with distinct visual hierarchies for user prompts, debate rounds, and verdicts. |
| **Motion Intent** | `4` | Tactile, micro-spring transitions (`120ms–180ms`). Zero gratuitous loaders or floating gimmick loops. |

**Atmosphere:** Deep Obsidian & Warm Zinc. Clinical yet warm, intentional, and high-performance — mimicking the Antigravity desktop IDE chat canvas.

---

## 2. Color Palette & Surface Elevation

```
Deep Canvas (#0B0D14) ──► Surface Base (#121520) ──► Surface Raised (#1A1E2D) ──► Surface Sunken (#07080D)
```

- **Canvas Background (`--bg`):** `#0B0D14` (Deep obsidian warm-neutral, avoiding blue glare or washed-out grays).
- **Surface Base (`--surface`):** `#121520` (Sidebar background, card fills, and panel backgrounds).
- **Surface Raised (`--surface-raised`):** `#1A1E2D` (Elevated cards, hover states, active selections, dropdown menus).
- **Surface Sunken (`--surface-sunken`):** `#07080D` (Textarea composer, nested code blocks, search inputs).
- **Whisper Border (`--border-subtle`):** `rgba(255, 255, 255, 0.08)` (Crisp 1px structural hair-lines).
- **Defined Border (`--border`):** `rgba(255, 255, 255, 0.16)` (Interactive inputs, active focus bounds).
- **Primary Text (`--fg`):** `#F3F4F6` (High contrast, readable against all dark surfaces).
- **Secondary Text (`--fg-muted`):** `#9CA3AF` (Descriptions, stage hints, helper text).
- **Tertiary Text (`--fg-subtle`):** `#6B7280` (Timestamps, metadata, collapsed labels).

### Accents & Signal Colors
- **Electric Accent (`--accent`):** `#3B82F6` (Electric Blue) / `#10B981` (Emerald Signal). Used for active states, CTA buttons, and focus rings.
- **Success Signal:** `#10B981` (Directive injected, completed checkmarks).
- **Warning / Steer Signal:** `#F59E0B` (Amber alerts, human steering directives, early conclusion banners).
- **Destructive Signal:** `#EF4444` (Delete project, remove key, errors).

---

## 3. Typography & Micro-Hierarchy

- **Primary UI Font (`--font-sans`):** `Geist`, `Inter`, system-ui, -apple-system, sans-serif. Track-tight (`letter-spacing: -0.015em`).
- **Code & Metadata Font (`--font-mono`):** `JetBrains Mono`, `Geist Mono`, ui-monospace, monospace. Used for timestamps, IDs, token counts, and debate telemetry.
- **Scale:**
  - Headers: `1.25rem` – `1.5rem` (600 semi-bold)
  - Base Body: `0.9375rem` (15px) for optimal long-form reading
  - Small / Hints: `0.8125rem` (13px)
  - Micro / Meta: `0.75rem` (12px hard floor)

---

## 4. Component Standards

### A. Left-Hand Sidebar (Workspace Tree)
- **Top CTA:** High-contrast `+ New Debate` button with instant keyboard shortcut hint (`Ctrl/⌘ + K`).
- **Section Headers:** Uppercase tracking (`0.05em`), muted slate (`#6B7280`), clean collapse toggles.
- **Folder Nodes:** Folder icon + project name + counter badge + hover actions (Add debate, Rename, Delete).
- **Debate Rows:**
  - Truncated single-line titles with message count.
  - Active indicator: Soft raised background + 2px left accent line.
  - Action tray on hover: Copy ID, ZIP Export, Inline Rename, Archive.
- **Bottom Drawer:** Collapsible "Archived Debates" drawer with restore triggers.

### B. Workspace Header & Breadcrumbs
- Minimal header with project folder path, conversation title, and clickable Conversation ID chip.
- Action group on right: Standalone Markdown Export (`FileText`) and Full Deliberation ZIP Export (`Package`).

### C. Live RunRail (Real-Time Progress)
- Sleek progress pill:
  - 4 stage nodes: `1 Positions` → `2 Debate` → `3 Review` → `4 Verdict`.
  - Done: Green checkmark badge. Active: Pulsing accent dot. Pending: Numeric index.
  - Live elapsed timer (`00m 42s`) and current round details.
  - Interactive **Steer Debate** button with inline collapsible directive injection form.

### D. The Verdict Hero (The Star Component)
- Styled as an executive report document:
  - Header: "The verdict", Chaired by model badge, tokens metric, failover badge (`⚡ Failover`), human-steered badge (`🎯 Human Steered`).
  - Section Cards: Decision, Reasoning, Tradeoffs, Dissent, Confidence.
  - Export bar at footer: Download report, download ZIP, toggle raw output.

### E. Floating Composer Bar
- Grounded at bottom with zero page bounce.
- Compact Model Roster badge bar showing seated model count, thinking levels, debate rounds, and token limits.
- Clean rounded textarea auto-expanding with keyboard shortcuts (`Enter` to send, `Shift+Enter` for newline).
- Tactile send button with loading state.

---

## 5. Performance, Ergonomics & Fast Handling

1. **Zero Window-Level Scrolling:** The root viewport is locked (`overflow: hidden; height: 100dvh`). Only the chat message container and sidebar conversation list scroll independently.
2. **Smooth Target Anchoring:** When submitting prompts or receiving verdicts, the view smoothly aligns to the top of the relevant card rather than dropping users into bottom empty space.
3. **Instant Keyboard Controls:**
   - `Enter` submits immediately.
   - `Shift + Enter` inserts newlines.
   - `Esc` closes modals (Provider Keys, Steer form).
4. **Lightweight Asset Footprint:**
   - Zero heavyweight icon libraries: uses native inline Lucide-style SVG vector components (`icons.jsx`).
   - Clean CSS variables with zero runtime CSS-in-JS overhead.
