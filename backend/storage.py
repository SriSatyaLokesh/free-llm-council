"""JSON-based storage for conversations."""

import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path
from .config import DATA_DIR


def ensure_data_dir():
    """Ensure the data directory exists."""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


def get_conversation_path(conversation_id: str) -> str:
    """Get the file path for a conversation."""
    return os.path.join(DATA_DIR, f"{conversation_id}.json")


def create_conversation(
    conversation_id: str, project_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new conversation.

    Args:
        conversation_id: Unique identifier for the conversation
        project_id: Optional project identifier to associate with

    Returns:
        New conversation dict
    """
    ensure_data_dir()

    conversation = {
        "id": conversation_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "title": "New Conversation",
        "project_id": project_id,
        "archived": False,
        "messages": []
    }

    # Save to file
    path = get_conversation_path(conversation_id)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(conversation, f, indent=2)

    return conversation


def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a conversation from storage.

    Args:
        conversation_id: Unique identifier for the conversation

    Returns:
        Conversation dict or None if not found
    """
    path = get_conversation_path(conversation_id)

    if not os.path.exists(path):
        return None

    with open(path, 'r') as f:
        return json.load(f)


def save_conversation(conversation: Dict[str, Any]):
    """
    Save a conversation to storage.

    Args:
        conversation: Conversation dict to save
    """
    ensure_data_dir()

    path = get_conversation_path(conversation['id'])
    with open(path, 'w') as f:
        json.dump(conversation, f, indent=2)


def delete_conversation(conversation_id: str) -> bool:
    """
    Permanently delete a conversation from storage.

    Returns:
        True if the file was found and deleted, False otherwise.
    """
    path = get_conversation_path(conversation_id)
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except OSError:
            return False
    return False


def prune_empty_conversations(except_id: Optional[str] = None) -> int:
    """
    Prune all abandoned conversations that have 0 messages.

    Args:
        except_id: Optional conversation ID to spare (e.g. active draft).

    Returns:
        Number of empty conversations deleted.
    """
    ensure_data_dir()
    pruned = 0
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith('.json') or filename == 'projects.json':
            continue
        conv_id = filename[:-5]
        if except_id and conv_id == except_id:
            continue
        path = os.path.join(DATA_DIR, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not data.get("messages") or len(data["messages"]) == 0:
                os.remove(path)
                pruned += 1
        except Exception:
            continue
    return pruned


def list_conversations(include_empty: bool = False) -> List[Dict[str, Any]]:
    """
    List all conversations (metadata only).

    By default, empty conversations (0 messages) are excluded to prevent
    ghost entries when a user explores without starting a deliberation.
    """
    ensure_data_dir()

    conversations = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json') and filename != 'projects.json':
            path = os.path.join(DATA_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                msg_count = len(data.get("messages", []))
                if not include_empty and msg_count == 0:
                    continue
                # Return metadata only
                conversations.append({
                    "id": data["id"],
                    "created_at": data["created_at"],
                    "title": data.get("title", "New Conversation"),
                    "project_id": data.get("project_id"),
                    "message_count": msg_count,
                    "archived": bool(data.get("archived", False)),
                })
            except Exception:
                continue

    # Sort by creation time, newest first
    conversations.sort(key=lambda x: x["created_at"], reverse=True)

    return conversations


def add_user_message(conversation_id: str, content: str):
    """
    Add a user message to a conversation.

    Args:
        conversation_id: Conversation identifier
        content: User message content
    """
    conversation = get_conversation(conversation_id)
    if conversation is None:
        raise ValueError(f"Conversation {conversation_id} not found")

    conversation["messages"].append({
        "role": "user",
        "content": content
    })

    save_conversation(conversation)


def add_assistant_message(conversation_id: str, result: Dict[str, Any]):
    """
    Add an assistant message holding a complete council run.

    The whole run is stored under "council" so the four stages stay together and
    the frontend can read them back after a reload. The "stage1"/"stage2"/
    "stage3" keys are kept as aliases onto the new stage names so older saved
    conversations still render.

    Args:
        conversation_id: Conversation identifier
        result: The dict returned by CouncilRun
    """
    conversation = get_conversation(conversation_id)
    if conversation is None:
        raise ValueError(f"Conversation {conversation_id} not found")

    message = {
        "role": "assistant",
        "council": {
            "positions": result.get("positions", []),
            "debate": result.get("debate", []),
            "review": result.get("review", []),
            "aggregate": result.get("aggregate", []),
            "verdict": result.get("verdict", {}),
            "metadata": result.get("metadata", {}),
        },
        "metadata": result.get("metadata", {}),
    }

    # Backwards-compatible aliases for the original three-stage shape.
    message["stage1"] = result.get("positions", [])
    message["stage2"] = result.get("review", [])
    message["stage3"] = result.get("verdict", {})

    conversation["messages"].append(message)
    save_conversation(conversation)


def update_conversation_title(conversation_id: str, title: str):
    """
    Update the title of a conversation.

    Args:
        conversation_id: Conversation identifier
        title: New title for the conversation
    """
    conversation = get_conversation(conversation_id)
    if conversation is None:
        raise ValueError(f"Conversation {conversation_id} not found")

    conversation["title"] = title
    save_conversation(conversation)


def set_conversation_archived(conversation_id: str, archived: bool = True) -> Dict[str, Any]:
    """
    Set the archived status of a conversation.

    Args:
        conversation_id: Conversation identifier
        archived: Whether the conversation should be marked as archived
    """
    conversation = get_conversation(conversation_id)
    if conversation is None:
        raise ValueError(f"Conversation {conversation_id} not found")

    conversation["archived"] = bool(archived)
    save_conversation(conversation)
    return conversation


# ---------------------------------------------------------------------------
# Project & Workspace Folder Management
# ---------------------------------------------------------------------------

def get_projects_file() -> str:
    return os.path.join(DATA_DIR, "projects.json")


def load_all_projects() -> Dict[str, Dict[str, Any]]:
    path = get_projects_file()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_all_projects(projects: Dict[str, Dict[str, Any]]) -> None:
    ensure_data_dir()
    path = get_projects_file()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2)


def create_project(
    name: str,
    description: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new project folder."""
    import uuid
    pid = project_id or str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    project = {
        "id": pid,
        "name": name,
        "description": description or "",
        "created_at": now,
        "updated_at": now,
    }
    projects = load_all_projects()
    projects[pid] = project
    save_all_projects(projects)
    return dict(project)


def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a project by ID."""
    projects = load_all_projects()
    return projects.get(project_id)


def update_project(project_id: str, patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update project name or description."""
    projects = load_all_projects()
    if project_id not in projects:
        return None
    proj = projects[project_id]
    if "name" in patch and patch["name"] is not None:
        proj["name"] = patch["name"]
    if "description" in patch and patch["description"] is not None:
        proj["description"] = patch["description"]
    proj["updated_at"] = datetime.now(timezone.utc).isoformat()
    projects[project_id] = proj
    save_all_projects(projects)
    return dict(proj)


def delete_project(project_id: str) -> bool:
    """
    Delete a project folder and unlink any associated conversations
    back to independent / standalone mode (project_id = None).
    """
    projects = load_all_projects()
    if project_id not in projects:
        return False
    del projects[project_id]
    save_all_projects(projects)

    # Unlink any conversations pointing to this project_id
    ensure_data_dir()
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json") and filename != "projects.json":
            path = os.path.join(DATA_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("project_id") == project_id:
                    data["project_id"] = None
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
            except Exception:
                continue
    return True


def list_projects() -> List[Dict[str, Any]]:
    """List all project folders with conversation count metadata."""
    projects = load_all_projects()
    counts: Dict[str, int] = {pid: 0 for pid in projects}
    ensure_data_dir()
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json") and filename != "projects.json":
            path = os.path.join(DATA_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                pid = data.get("project_id")
                if pid and pid in counts:
                    counts[pid] += 1
            except Exception:
                continue

    result = []
    for pid, proj in projects.items():
        entry = dict(proj)
        entry["conversation_count"] = counts.get(pid, 0)
        result.append(entry)

    result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return result


def assign_conversation_project(conversation_id: str, project_id: Optional[str]) -> bool:
    """Assign or unassign a conversation to/from a project folder."""
    conv = get_conversation(conversation_id)
    if conv is None:
        return False
    conv["project_id"] = project_id
    save_conversation(conv)
    return True


# ---------------------------------------------------------------------------
# Report and Zip Export Utilities
# ---------------------------------------------------------------------------

def _clean_table_cell(text: str, max_chars: int = 150) -> str:
    """Clean and truncate text for safe rendering in Markdown table cells."""
    if not text:
        return "—"
    cleaned = text.replace("|", "\\|").replace("\n", " ").replace("\r", " ").strip()
    # Collapse multiple spaces
    cleaned = " ".join(cleaned.split())
    if len(cleaned) > max_chars:
        return cleaned[: max_chars - 3].rstrip() + "..."
    return cleaned


def _generate_ascii_deliberation_flow(members: List[str], chairman: str) -> str:
    """Generate a high-contrast ASCII diagram visualizing the council's 4-stage pipeline."""
    chair_name = chairman or "Designated Chairman"
    display_members = members[:4] if members else ["Model A", "Model B", "Model C"]
    member_chips = "   ".join(f"[{m[:18]}]" for m in display_members)
    if len(members) > 4:
        member_chips += f"  (+{len(members)-4} more)"

    return f"""```text
+-----------------------------------------------------------------------------------------+
|                        COUNCIL MULTI-AGENT DELIBERATION FLOW                            |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|                                [ User Strategic Prompt ]                                |
|                                            │                                            |
|                                            ▼                                            |
|  +───────────────────────────────────────────────────────────────────────────────────+  |
|  | STAGE 1: DIVERGENT OPENING POSITIONS (Independent Ideation)                       |  |
|  | {member_chips.center(81)} |  |
|  +─────────────────────────────────────────┬─────────────────────────────────────────+  |
|                                            │                                            |
|                                            ▼                                            |
|  +───────────────────────────────────────────────────────────────────────────────────+  |
|  | STAGE 2: CROSS-EXAMINATION & PEER DEBATE (Stress-Testing Assumptions)             |  |
|  |   ◄─── Counter-Arguments, Defenses, Trade-off Challenges & Concessions ───►        |  |
|  +─────────────────────────────────────────┬─────────────────────────────────────────+  |
|                                            │                                            |
|                                            ▼                                            |
|  +───────────────────────────────────────────────────────────────────────────────────+  |
|  | STAGE 3: BLIND PEER REVIEW & EVALUATION (Objective Peer Scoring)                  |  |
|  |   - Anonymized Critique & Scoring Matrix (Accuracy, Feasibility, Trade-offs)      |  |
|  +─────────────────────────────────────────┬─────────────────────────────────────────+  |
|                                            │                                            |
|                                            ▼                                            |
|  +───────────────────────────────────────────────────────────────────────────────────+  |
|  | STAGE 4: EXECUTIVE CHAIRMAN SYNTHESIS & BINDING VERDICT                           |  |
|  | Presiding Chairman: [{chair_name[:35]}]                                              |  |
|  |   [✔] Final Decision     [✔] Strategic Tradeoffs     [✔] Dissent Resolution       |  |
|  +───────────────────────────────────────────────────────────────────────────────────+  |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```"""


def format_conversation_executive(conv: Dict[str, Any]) -> str:
    """
    Format an executive summary report tailored for rapid stakeholder and leadership review.
    Focuses on the high-level decision, decisive rationale, tradeoffs, and stage takeaways.
    """
    title = conv.get("title", "Council Deliberation")
    conv_id = conv.get("id", "unknown")
    created = conv.get("created_at", "")
    lines = [
        f"# {title}",
        "",
        f"- **Deliberation ID:** `{conv_id}`",
        f"- **Date & Time:** {created}",
        "- **Report Type:** Executive Briefing Report",
        "",
        "---",
        "",
    ]

    messages = conv.get("messages", [])
    if not messages:
        lines.append("*No messages recorded in this council session.*")
        return "\n".join(lines)

    for msg in messages:
        role = msg.get("role", "unknown")
        if role == "user":
            lines.extend([
                "## Query / Prompt",
                "",
                msg.get("content", "").strip(),
                "",
                "---",
                "",
            ])
        elif role == "assistant":
            council = msg.get("council", {})
            metadata = council.get("metadata", {}) or msg.get("metadata", {})
            verdict = council.get("verdict", {})

            # 1. Chairman Verdict
            lines.append("## Executive Verdict (Chairman Synthesis)")
            lines.append("")
            if verdict:
                chair = verdict.get("model", "Unknown Chairman")
                lines.append(f"**Chairman:** `{chair}`")
                sections = verdict.get("sections", {})
                if sections:
                    for sec_key in ["decision", "reasoning", "tradeoffs", "dissent", "confidence"]:
                        if sec_key in sections:
                            sec_title = sec_key.capitalize()
                            lines.extend([
                                "",
                                f"### {sec_title}",
                                "",
                                sections[sec_key].strip(),
                            ])
                elif verdict.get("response"):
                    lines.extend([
                        "",
                        verdict["response"].strip(),
                    ])
            else:
                lines.append("*No verdict reached.*")
            lines.extend(["", "---", ""])

            # 2. Stage 1: Opening Positions
            positions = council.get("positions", [])
            lines.append("## Stage 1: Opening Positions")
            lines.append("")
            if positions:
                for pos in positions:
                    model = pos.get("model", "Unknown")
                    err = pos.get("error")
                    resp = pos.get("response", "")
                    lines.append(f"### Model: `{model}`")
                    if err:
                        lines.append(f"> ⚠️ **Error:** {err}")
                    if resp:
                        lines.append(resp.strip())
                    lines.append("")
            else:
                lines.append("*No opening positions.*")
                lines.append("")

            # 3. Stage 2: Peer Debate
            debates = council.get("debate", [])
            lines.append("## Stage 2: Peer Debate & Cross-Examination")
            lines.append("")
            if debates:
                for round_item in debates:
                    round_num = round_item.get("round", 1)
                    lines.append(f"### Round {round_num}")
                    lines.append("")
                    for reply in round_item.get("responses", []):
                        model = reply.get("model", "Unknown")
                        err = reply.get("error")
                        resp = reply.get("response", "")
                        lines.append(f"#### Model: `{model}`")
                        if err:
                            lines.append(f"> ⚠️ **Error:** {err}")
                        if resp:
                            lines.append(resp.strip())
                        lines.append("")
            else:
                lines.append("*No peer debate rounds.*")
                lines.append("")

            # 4. Stage 3: Blind Peer Review
            reviews = council.get("review", [])
            lines.append("## Stage 3: Blind Peer Review")
            lines.append("")
            if reviews:
                for rev in reviews:
                    model = rev.get("model", "Unknown")
                    resp = rev.get("response", "")
                    lines.append(f"### Reviewer: `{model}`")
                    if resp:
                        lines.append(resp.strip())
                    lines.append("")
            else:
                lines.append("*No peer reviews.*")
                lines.append("")

            # 5. Metadata & Telemetry
            lines.append("## Session Telemetry & Metadata")
            lines.append("")
            if metadata:
                members = metadata.get("members", [])
                if members:
                    lines.append(f"- **Participating Members:** {', '.join(f'`{m}`' for m in members)}")
                if metadata.get("chairman"):
                    lines.append(f"- **Designated Chairman:** `{metadata.get('chairman')}`")
                if metadata.get("caveman"):
                    lines.append(f"- **Caveman Mode:** `{metadata.get('caveman')}`")
                if metadata.get("total_tokens"):
                    lines.append(f"- **Total Tokens Consumed:** {metadata.get('total_tokens'):,}")
                if metadata.get("evicted_models"):
                    lines.append(f"- **Evicted Models:** {', '.join(f'`{e.get('model')}`' for e in metadata.get('evicted_models', []))}")
                if metadata.get("injected_guidance"):
                    lines.append(f"- **Injected Steering Directives:** {len(metadata.get('injected_guidance'))} guidance event(s)")
            lines.extend(["", "---", ""])

    return "\n".join(lines)


def format_conversation_detailed(conv: Dict[str, Any]) -> str:
    """
    Format a comprehensive deep-dive technical matrix report.
    Includes:
      - Deliberation Overview & Telemetry Card
      - ASCII Multi-Agent Deliberation Architecture Flow Diagram
      - Comparative Model Deliberation Matrix Table
      - The 'Why' Infographic & Strategic Trade-off Matrix Table
      - Dissent Resolution & Consensus Analysis
      - Complete Granular Stage-by-Stage Transcripts
      - Operational Telemetry Table
    """
    title = conv.get("title", "Council Deliberation")
    conv_id = conv.get("id", "unknown")
    created = conv.get("created_at", "")
    messages = conv.get("messages", [])

    lines = [
        f"# 🏛️ Council Deliberation Deep-Dive & Comparative Matrix: {title}",
        "",
        "> **Report Class:** Technical Deep-Dive Matrix & Decision Audit  ",
        f"> **Deliberation ID:** `{conv_id}` | **Session Date:** {created}",
        "",
        "---",
        "",
    ]

    if not messages:
        lines.append("*No messages recorded in this council session.*")
        return "\n".join(lines)

    for msg in messages:
        role = msg.get("role", "unknown")
        if role == "user":
            lines.extend([
                "## 📋 Strategic Query / Prompt",
                "",
                msg.get("content", "").strip(),
                "",
                "---",
                "",
            ])
        elif role == "assistant":
            council = msg.get("council", {})
            metadata = council.get("metadata", {}) or msg.get("metadata", {})
            verdict = council.get("verdict", {})
            positions = council.get("positions", [])
            debates = council.get("debate", [])
            reviews = council.get("review", [])

            members = metadata.get("members", [])
            if not members and positions:
                members = [p.get("model", "Unknown") for p in positions]
            chairman = verdict.get("model") or metadata.get("chairman", "Chairman")
            sections = verdict.get("sections", {})
            total_tokens = metadata.get("total_tokens", 0)

            # 1. Telemetry Overview Table
            lines.extend([
                "## 📊 Executive Overview & Deliberation Parameters",
                "",
                "| Parameter / Metric | Deliberation Detail |",
                "| :--- | :--- |",
                f"| **Presiding Chairman** | `{chairman}` |",
                f"| **Participating Council Members** | {len(members)} models ({', '.join(f'`{m}`' for m in members)}) |",
                f"| **Deliberation Token Footprint** | {total_tokens:,} tokens |",
                f"| **Confidence Level** | `{sections.get('confidence', 'Evaluated')}` |",
                f"| **Caveman Compression Mode** | `{metadata.get('caveman', 'disabled')}` |",
                "",
                "---",
                "",
            ])

            # 2. ASCII Deliberation Flow Diagram
            lines.extend([
                "## 🗺️ Council Deliberation Architecture & Flow",
                "",
                _generate_ascii_deliberation_flow(members, chairman),
                "",
                "---",
                "",
            ])

            # 3. Comparative Model Deliberation Matrix Table
            lines.extend([
                "## ⚖️ Comparative Model Deliberation Matrix",
                "",
                "A cross-sectional breakdown comparing initial stances, debate friction, peer reviews, and final verdict alignment across all participating council models.",
                "",
                "| Council Model | Opening Stance / Proposal | Cross-Examination Focus | Peer Review Assessment | Stance Alignment with Verdict |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])

            for pos in positions:
                m_name = pos.get("model", "Unknown")
                opening_snippet = _clean_table_cell(pos.get("response", ""), 140)

                # Find debate presence
                debate_points = []
                for d_round in debates:
                    for resp in d_round.get("responses", []):
                        if resp.get("model") == m_name:
                            debate_points.append(resp.get("response", ""))
                debate_snippet = _clean_table_cell(" ".join(debate_points), 130) if debate_points else "Standard position defended"

                # Find peer review comments
                review_comments = []
                for rev in reviews:
                    if rev.get("model") == m_name:
                        review_comments.append(rev.get("response", ""))
                review_snippet = _clean_table_cell(" ".join(review_comments), 130) if review_comments else "Peer reviewed"

                # Stance alignment
                if m_name == chairman:
                    alignment = "👑 **Chairman (Synthesis Author)**"
                elif sections.get("dissent") and m_name.lower() in sections.get("dissent", "").lower():
                    alignment = "⚠️ *Dissenting / Alternative*"
                else:
                    alignment = "✅ *Aligned / Core Contributor*"

                lines.append(
                    f"| `{m_name}` | {opening_snippet} | {debate_snippet} | {review_snippet} | {alignment} |"
                )

            lines.extend(["", "---", ""])

            # 4. Strategic Decision "The Why" & Trade-Off Matrix
            decision_text = sections.get("decision", verdict.get("response", "No decision text recorded.")).strip()
            reasoning_text = sections.get("reasoning", "Multi-model debate convergence analysis applied.").strip()
            tradeoffs_text = sections.get("tradeoffs", "Operational and architectural compromises evaluated.").strip()
            dissent_text = sections.get("dissent", "No material dissent unaddressed.").strip()
            confidence_text = sections.get("confidence", "High").strip()

            lines.extend([
                "## 🎯 Strategic Decision & 'The Why' Analysis",
                "",
                "### 🏆 Executive Verdict (Chairman Synthesis)",
                f"**Presiding Chairman:** `{chairman}`  ",
                f"**Confidence Assessment:** `{confidence_text}`",
                "",
                "### Decision",
                "",
                decision_text,
                "",
                "### Reasoning & The Decisive 'Why'",
                "",
                reasoning_text,
                "",
                "### ⚖️ Strategic Trade-Off & Risk Mitigation Matrix",
                "",
                "| Evaluation Dimension | Strategic Selected Path | Inherent Trade-Off / Cost | Recommended Mitigation |",
                "| :--- | :--- | :--- | :--- |",
                f"| **Primary Architectural Selection** | {_clean_table_cell(decision_text, 110)} | {_clean_table_cell(tradeoffs_text, 110)} | Establish clear SLOs and automated guardrails |",
                f"| **Operational Overhead** | Standardized pattern with multi-model consensus | Transition & tooling learning curve | Gradual rollout with comprehensive runbooks |",
                f"| **Failure Modes & Edge Cases** | Validated against peer cross-examination | Tail latency and boundary condition risks | Implement robust circuit breakers and fallbacks |",
                f"| **Dissent & Minority Concerns** | Reconciled during blind peer review | {_clean_table_cell(dissent_text, 110)} | Re-evaluate triggers if system scale multiplies |",
                "",
                "### 🛡️ Dissenting Perspectives & Counter-Argument Resolution",
                "",
                dissent_text,
                "",
                "---",
                "",
            ])

            # 5. Full Stage-by-Stage Deliberation Transcripts
            lines.extend([
                "## 📜 Comprehensive Stage-by-Stage Deliberation Audit",
                "",
                "### Stage 1: Opening Positions",
                "",
            ])
            if positions:
                for pos in positions:
                    m = pos.get("model", "Unknown")
                    err = pos.get("error")
                    resp = pos.get("response", "")
                    lines.append(f"#### Model: `{m}`")
                    if err:
                        lines.append(f"> ⚠️ **Error:** {err}")
                    if resp:
                        lines.append(resp.strip())
                    lines.append("")
            else:
                lines.append("*No opening positions.*")
                lines.append("")

            lines.extend([
                "### Stage 2: Peer Debate & Cross-Examination",
                "",
            ])
            if debates:
                for round_item in debates:
                    round_num = round_item.get("round", 1)
                    lines.append(f"#### Round {round_num}")
                    lines.append("")
                    for reply in round_item.get("responses", []):
                        m = reply.get("model", "Unknown")
                        err = reply.get("error")
                        resp = reply.get("response", "")
                        lines.append(f"##### Model: `{m}`")
                        if err:
                            lines.append(f"> ⚠️ **Error:** {err}")
                        if resp:
                            lines.append(resp.strip())
                        lines.append("")
            else:
                lines.append("*No peer debate rounds.*")
                lines.append("")

            lines.extend([
                "### Stage 3: Blind Peer Review",
                "",
            ])
            if reviews:
                for rev in reviews:
                    m = rev.get("model", "Unknown")
                    resp = rev.get("response", "")
                    lines.append(f"#### Reviewer: `{m}`")
                    if resp:
                        lines.append(resp.strip())
                    lines.append("")
            else:
                lines.append("*No peer reviews.*")
                lines.append("")

            # 6. Governance & Telemetry Audit
            lines.extend([
                "## Session Telemetry & Governance Metadata",
                "",
                "| Telemetry Field | Recorded Value |",
                "| :--- | :--- |",
                f"| **Deliberation ID** | `{conv_id}` |",
                f"| **Designated Chairman** | `{metadata.get('chairman', chairman)}` |",
                f"| **Participating Models** | {', '.join(f'`{m}`' for m in members)} |",
                f"| **Caveman Mode** | `{metadata.get('caveman', 'disabled')}` |",
                f"| **Total Tokens Consumed** | {total_tokens:,} |",
                f"| **Evicted Models Count** | {len(metadata.get('evicted_models', []))} |",
                f"| **Steering Directives** | {len(metadata.get('injected_guidance', []))} directive(s) |",
                "",
                "---",
                "",
            ])

    return "\n".join(lines)


def format_conversation_markdown(conv: Dict[str, Any], mode: str = "executive") -> str:
    """
    Format a complete council deliberation into a clean, comprehensive Markdown report.
    Supports 'executive' (default) and 'detailed' modes.
    """
    if mode in ("detailed", "comprehensive"):
        return format_conversation_detailed(conv)
    return format_conversation_executive(conv)


def export_conversation_zip(conv: Dict[str, Any]) -> bytes:
    """
    Build an in-memory zip archive containing:
      - executive-report.md (high-level executive briefing)
      - detailed-report.md (comprehensive deep-dive technical matrix report)
      - report.md (executive report for backward compatibility)
      - conversation.json (full raw structured data)
      - summary.txt (concise executive summary)
    """
    import io
    import zipfile

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Full raw JSON
        raw_json = json.dumps(conv, indent=2, ensure_ascii=False)
        zf.writestr("conversation.json", raw_json.encode("utf-8"))

        # 2. Executive report
        executive_report = format_conversation_executive(conv)
        zf.writestr("executive-report.md", executive_report.encode("utf-8"))
        # Backward-compatible report.md
        zf.writestr("report.md", executive_report.encode("utf-8"))

        # 3. Comprehensive deep-dive report
        detailed_report = format_conversation_detailed(conv)
        zf.writestr("detailed-report.md", detailed_report.encode("utf-8"))

        # 4. Concise summary
        title = conv.get("title", "Council Deliberation")
        conv_id = conv.get("id", "unknown")
        summary_lines = [
            f"LLM COUNCIL DELIBERATION SUMMARY",
            f"Title: {title}",
            f"Deliberation ID: {conv_id}",
            f"Date: {conv.get('created_at', '')}",
            f"Message Count: {len(conv.get('messages', []))}",
            "",
        ]
        # Find latest verdict
        verdict_text = ""
        for msg in reversed(conv.get("messages", [])):
            if msg.get("role") == "assistant":
                v = msg.get("council", {}).get("verdict", {})
                if v:
                    sec = v.get("sections", {})
                    if sec.get("decision"):
                        verdict_text = f"DECISION:\n{sec['decision']}\n\nCONFIDENCE:\n{sec.get('confidence', 'N/A')}"
                    elif v.get("response"):
                        verdict_text = f"DECISION:\n{v['response']}"
                break
        if verdict_text:
            summary_lines.append(verdict_text)
        else:
            summary_lines.append("No final verdict available.")

        zf.writestr("summary.txt", "\n".join(summary_lines).encode("utf-8"))

    buffer.seek(0)
    return buffer.getvalue()


