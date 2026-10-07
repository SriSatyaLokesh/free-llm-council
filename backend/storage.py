"""JSON-based storage for conversations."""

import json
import os
import shutil
import subprocess
import tempfile
import platform
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
        return "--"
    # Replace pipes with dashes to prevent breaking Markdown table column delimiters
    cleaned = text.replace("|", " - ").replace("\n", " ").replace("\r", " ").strip()
    # Collapse multiple spaces
    cleaned = " ".join(cleaned.split())
    if len(cleaned) > max_chars:
        cleaned = cleaned[: max_chars - 3].rstrip() + "..."
    while cleaned.endswith("\\"):
        cleaned = cleaned[:-1].rstrip()
    return cleaned


def _generate_ascii_deliberation_flow(members: List[str], chairman: str) -> str:
    """Generate a clean ASCII diagram visualizing the council's 4-stage pipeline."""
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
|                                            |                                            |
|                                            v                                            |
|  +-----------------------------------------------------------------------------------+  |
|  | STAGE 1: DIVERGENT OPENING POSITIONS (Independent Ideation)                       |  |
|  | {member_chips.center(81)} |  |
|  +-----------------------------------------+-----------------------------------------+  |
|                                            |                                            |
|                                            v                                            |
|  +-----------------------------------------------------------------------------------+  |
|  | STAGE 2: CROSS-EXAMINATION & PEER DEBATE (Stress-Testing Assumptions)             |  |
|  |   <--- Counter-Arguments, Defenses, Trade-off Challenges & Concessions --->        |  |
|  +-----------------------------------------+-----------------------------------------+  |
|                                            |                                            |
|                                            v                                            |
|  +-----------------------------------------------------------------------------------+  |
|  | STAGE 3: BLIND PEER REVIEW & EVALUATION (Objective Peer Scoring)                  |  |
|  |   - Anonymized Critique & Scoring Matrix (Accuracy, Feasibility, Trade-offs)      |  |
|  +-----------------------------------------+-----------------------------------------+  |
|                                            |                                            |
|                                            v                                            |
|  +-----------------------------------------------------------------------------------+  |
|  | STAGE 4: EXECUTIVE CHAIRMAN SYNTHESIS & BINDING VERDICT                           |  |
|  | Presiding Chairman: [{chair_name[:35]}]                                              |  |
|  |   [+] Final Decision     [+] Strategic Tradeoffs     [+] Dissent Resolution       |  |
|  +-----------------------------------------------------------------------------------+  |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```"""


def _extract_non_reporting_models(council: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract models that failed to report, timed out, or were evicted from deliberation.
    Returns mapping of model_name -> failure reason string.
    """
    non_reporting: Dict[str, str] = {}

    evicted_list = metadata.get("evicted_members") or metadata.get("evicted_models") or []
    for ev in evicted_list:
        m = ev.get("model")
        if m:
            non_reporting[m] = ev.get("reason") or "Failed to report / evicted from deliberation"

    positions = council.get("positions", [])
    for pos in positions:
        m = pos.get("model")
        err = pos.get("error")
        resp = (pos.get("response") or "").strip()
        tool_calls = pos.get("toolCalls") or []
        if err or (not resp and not tool_calls):
            if m and m not in non_reporting:
                non_reporting[m] = err or "Timed out / returned empty position"

    requested = metadata.get("requested_members", [])
    members = metadata.get("members", [])
    for req in requested:
        if req not in non_reporting:
            has_reported = any(
                p.get("model") == req and (p.get("response") or p.get("toolCalls")) and not p.get("error")
                for p in positions
            )
            if not has_reported and req not in members:
                non_reporting[req] = "Did not report to council (initialization failed / unreachable)"

    return non_reporting


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
            non_reporting = _extract_non_reporting_models(council, metadata)

            # State missing/timed-out agents prominently on top once
            if non_reporting:
                lines.extend([
                    "> **Council Attendance Notice:** The following agent(s) did not report to the council or timed out and were excluded from deliberation:",
                ])
                for m, reason in non_reporting.items():
                    lines.append(f"> - `{m}`: {reason}")
                lines.extend([
                    "> Deliberation proceeded with active council members.",
                    "",
                    "---",
                    "",
                ])

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

            # 2. Stage 1: Opening Positions (only reporting members)
            positions = council.get("positions", [])
            valid_positions = [
                p for p in positions
                if p.get("model") not in non_reporting and not p.get("error") and (p.get("response") or p.get("toolCalls"))
            ]
            lines.append("## Stage 1: Opening Positions")
            lines.append("")
            if valid_positions:
                for pos in valid_positions:
                    model = pos.get("model", "Unknown")
                    resp = pos.get("response", "")
                    lines.append(f"### Model: `{model}`")
                    if resp:
                        lines.append(resp.strip())
                    lines.append("")
            else:
                lines.append("*No opening positions.*")
                lines.append("")

            # 3. Stage 2: Peer Debate (only reporting members)
            debates = council.get("debate", [])
            lines.append("## Stage 2: Peer Debate & Cross-Examination")
            lines.append("")
            if debates:
                for round_item in debates:
                    round_num = round_item.get("round", 1)
                    raw_replies = round_item.get("statements", round_item.get("responses", []))
                    valid_replies = [
                        reply for reply in raw_replies
                        if reply.get("model") not in non_reporting and not reply.get("error") and reply.get("response")
                    ]
                    if valid_replies:
                        lines.append(f"### Round {round_num}")
                        lines.append("")
                        for reply in valid_replies:
                            model = reply.get("model", "Unknown")
                            resp = reply.get("response", "")
                            lines.append(f"#### Model: `{model}`")
                            if resp:
                                lines.append(resp.strip())
                            lines.append("")
            else:
                lines.append("*No peer debate rounds.*")
                lines.append("")

            # 4. Stage 3: Blind Peer Review (only reporting members)
            reviews = council.get("review", [])
            valid_reviews = [
                rev for rev in reviews
                if rev.get("model") not in non_reporting and not rev.get("error") and (rev.get("ranking") or rev.get("response"))
            ]
            lines.append("## Stage 3: Blind Peer Review")
            lines.append("")
            if valid_reviews:
                for rev in valid_reviews:
                    model = rev.get("model", "Unknown")
                    resp = rev.get("ranking") or rev.get("response", "")
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
                raw_members = metadata.get("members", []) or [p.get("model") for p in valid_positions]
                active_members = [m for m in raw_members if m not in non_reporting]
                if active_members:
                    lines.append(f"- **Participating Quorum:** {', '.join(f'`{m}`' for m in active_members)}")
                if non_reporting:
                    lines.append(f"- **Non-Reporting Members:** {', '.join(f'`{m}`' for m in non_reporting)}")
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
        f"# Council Deliberation Deep-Dive & Comparative Matrix: {title}",
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
                "## Strategic Query / Prompt",
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
            non_reporting = _extract_non_reporting_models(council, metadata)

            valid_positions = [
                p for p in positions
                if p.get("model") not in non_reporting and not p.get("error") and (p.get("response") or p.get("toolCalls"))
            ]

            raw_members = metadata.get("members", []) or [p.get("model") for p in valid_positions]
            active_members = [m for m in raw_members if m not in non_reporting]
            if not active_members and valid_positions:
                active_members = [p.get("model", "Unknown") for p in valid_positions]

            chairman = verdict.get("model") or metadata.get("chairman", "Chairman")
            sections = verdict.get("sections", {})
            total_tokens = metadata.get("total_tokens", 0)

            # State missing/timed-out agents prominently on top once
            if non_reporting:
                lines.extend([
                    "> **Council Attendance Notice:** The following agent(s) did not report to the council or timed out and were excluded from deliberation:",
                ])
                for m, reason in non_reporting.items():
                    lines.append(f"> - `{m}`: {reason}")
                lines.extend([
                    "> Deliberation proceeded with active council members.",
                    "",
                    "---",
                    "",
                ])

            # 1. Telemetry Overview Table
            telemetry_rows = [
                "## Executive Overview & Deliberation Parameters",
                "",
                "| Parameter / Metric | Deliberation Detail |",
                "| :--- | :--- |",
                f"| **Presiding Chairman** | `{chairman}` |",
                f"| **Active Council Quorum** | {len(active_members)} models ({', '.join(f'`{m}`' for m in active_members)}) |",
            ]
            if non_reporting:
                telemetry_rows.append(
                    f"| **Non-Reporting Members** | {len(non_reporting)} model(s) ({', '.join(f'`{m}`' for m in non_reporting)}) |"
                )
            telemetry_rows.extend([
                f"| **Deliberation Token Footprint** | {total_tokens:,} tokens |",
                f"| **Confidence Level** | `{sections.get('confidence', 'Evaluated')}` |",
                f"| **Caveman Compression Mode** | `{metadata.get('caveman', 'disabled')}` |",
                "",
                "---",
                "",
            ])
            lines.extend(telemetry_rows)

            # 2. ASCII Deliberation Flow Diagram
            lines.extend([
                "## Council Deliberation Architecture & Flow",
                "",
                _generate_ascii_deliberation_flow(active_members, chairman),
                "",
                "---",
                "",
            ])

            # 3. Comparative Model Deliberation Matrix Table
            lines.extend([
                "## Comparative Model Deliberation Matrix",
                "",
                "A cross-sectional breakdown comparing initial stances, debate friction, peer reviews, and final verdict alignment across all participating council models.",
                "",
                "| Council Model | Opening Stance / Proposal | Cross-Examination Focus | Peer Review Assessment | Stance Alignment with Verdict |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])

            for pos in valid_positions:
                m_name = pos.get("model", "Unknown")
                opening_snippet = _clean_table_cell(pos.get("response", ""), 140)

                # Find debate presence
                debate_points = []
                for d_round in debates:
                    round_replies = d_round.get("statements", d_round.get("responses", []))
                    for resp in round_replies:
                        if resp.get("model") == m_name and not resp.get("error") and resp.get("response"):
                            debate_points.append(resp.get("response", ""))
                debate_snippet = _clean_table_cell(" ".join(debate_points), 130) if debate_points else "Standard position defended"

                # Find peer review comments
                review_comments = []
                for rev in reviews:
                    if rev.get("model") == m_name and not rev.get("error"):
                        txt = rev.get("ranking") or rev.get("response", "")
                        if txt:
                            review_comments.append(txt)
                review_snippet = _clean_table_cell(" ".join(review_comments), 130) if review_comments else "Peer reviewed"

                # Stance alignment
                if m_name == chairman:
                    alignment = "**Chairman (Synthesis Author)**"
                elif sections.get("dissent") and m_name.lower() in sections.get("dissent", "").lower():
                    alignment = "*Dissenting / Alternative*"
                else:
                    alignment = "*Aligned / Core Contributor*"

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
                "## Strategic Decision & Justification",
                "",
                "### Executive Verdict (Chairman Synthesis)",
                f"**Presiding Chairman:** `{chairman}`  ",
                f"**Confidence Assessment:** `{confidence_text}`",
                "",
                "### Decision",
                "",
                decision_text,
                "",
                "### Reasoning & The Decisive Justification",
                "",
                reasoning_text,
                "",
                "### Strategic Trade-Off & Risk Mitigation Matrix",
                "",
                "| Evaluation Dimension | Strategic Selected Path | Inherent Trade-Off / Cost | Recommended Mitigation |",
                "| :--- | :--- | :--- | :--- |",
                f"| **Primary Architectural Selection** | {_clean_table_cell(decision_text, 110)} | {_clean_table_cell(tradeoffs_text, 110)} | Establish clear SLOs and automated guardrails |",
                f"| **Operational Overhead** | Standardized pattern with multi-model consensus | Transition & tooling learning curve | Gradual rollout with comprehensive runbooks |",
                f"| **Failure Modes & Edge Cases** | Validated against peer cross-examination | Tail latency and boundary condition risks | Implement robust circuit breakers and fallbacks |",
                f"| **Dissent & Minority Concerns** | Reconciled during blind peer review | {_clean_table_cell(dissent_text, 110)} | Re-evaluate triggers if system scale multiplies |",
                "",
                "### Dissenting Perspectives & Counter-Argument Resolution",
                "",
                dissent_text,
                "",
                "---",
                "",
            ])

            # 5. Full Stage-by-Stage Deliberation Transcripts (only reporting members)
            lines.extend([
                "## Comprehensive Stage-by-Stage Deliberation Audit",
                "",
                "### Stage 1: Opening Positions",
                "",
            ])
            if valid_positions:
                for pos in valid_positions:
                    m = pos.get("model", "Unknown")
                    resp = pos.get("response", "")
                    lines.append(f"#### Model: `{m}`")
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
                    raw_replies = round_item.get("statements", round_item.get("responses", []))
                    valid_replies = [
                        reply for reply in raw_replies
                        if reply.get("model") not in non_reporting and not reply.get("error") and reply.get("response")
                    ]
                    if valid_replies:
                        lines.append(f"#### Round {round_num}")
                        lines.append("")
                        for reply in valid_replies:
                            m = reply.get("model", "Unknown")
                            resp = reply.get("response", "")
                            lines.append(f"##### Model: `{m}`")
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
            valid_reviews = [
                rev for rev in reviews
                if rev.get("model") not in non_reporting and not rev.get("error") and (rev.get("ranking") or rev.get("response"))
            ]
            if valid_reviews:
                for rev in valid_reviews:
                    m = rev.get("model", "Unknown")
                    resp = rev.get("ranking") or rev.get("response", "")
                    lines.append(f"#### Reviewer: `{m}`")
                    if resp:
                        lines.append(resp.strip())
                    lines.append("")
            else:
                lines.append("*No peer reviews.*")
                lines.append("")

            # 6. Governance & Telemetry Audit
            audit_rows = [
                "## Session Telemetry & Governance Metadata",
                "",
                "| Telemetry Field | Recorded Value |",
                "| :--- | :--- |",
                f"| **Deliberation ID** | `{conv_id}` |",
                f"| **Designated Chairman** | `{metadata.get('chairman', chairman)}` |",
                f"| **Active Quorum Models** | {', '.join(f'`{m}`' for m in active_members)} |",
            ]
            if non_reporting:
                audit_rows.append(
                    f"| **Non-Reporting Models** | {', '.join(f'`{m}`' for m in non_reporting)} |"
                )
            audit_rows.extend([
                f"| **Caveman Mode** | `{metadata.get('caveman', 'disabled')}` |",
                f"| **Total Tokens Consumed** | {total_tokens:,} |",
                f"| **Non-Reporting Count** | {len(non_reporting)} |",
                f"| **Steering Directives** | {len(metadata.get('injected_guidance', []))} directive(s) |",
                "",
                "---",
                "",
            ])
            lines.extend(audit_rows)

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

        # 5. Standalone publication-grade HTML reports
        try:
            exec_html = render_report_html(conv, mode="executive")
            zf.writestr("executive-report.html", exec_html.encode("utf-8"))
            detailed_html = render_report_html(conv, mode="detailed")
            zf.writestr("detailed-report.html", detailed_html.encode("utf-8"))
        except Exception:
            pass

        # 6. Standalone publication-grade PDF reports (if headless engine is present)
        try:
            exec_pdf = generate_report_pdf(conv, mode="executive")
            if exec_pdf:
                zf.writestr("executive-report.pdf", exec_pdf)
            detailed_pdf = generate_report_pdf(conv, mode="detailed")
            if detailed_pdf:
                zf.writestr("detailed-report.pdf", detailed_pdf)
        except Exception:
            pass

    buffer.seek(0)
    return buffer.getvalue()


def find_headless_browser() -> Optional[str]:
    """
    Detect an available headless browser executable (Edge, Chrome, Chromium)
    on the host system.
    """
    # 1. Windows standard installation locations
    if platform.system() == "Windows":
        common_win_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ]
        for p in common_win_paths:
            if os.path.isfile(p):
                return p

    # 2. PATH resolution
    candidates = [
        "msedge",
        "chrome",
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
    ]
    for c in candidates:
        found = shutil.which(c)
        if found and os.path.isfile(found):
            return found

    # 3. macOS / Linux standard locations
    unix_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for p in unix_paths:
        if os.path.isfile(p):
            return p

    return None


def render_report_html(conv: Dict[str, Any], mode: str = "executive") -> str:
    """
    Render a deliberation conversation as a publication-grade standalone HTML document
    with comprehensive print/PDF styling and zero emojis.
    """
    import markdown_it

    title = conv.get("title", "Council Deliberation")
    conv_id = conv.get("id", "unknown")
    created_at = conv.get("created_at", "")
    mode_title = (
        "Executive Summary Brief"
        if mode in ("executive", "brief")
        else "Comprehensive Deep-Dive Technical Matrix"
    )

    # Extract metadata metrics
    chairman = "Unknown"
    members_count = "N/A"
    confidence = "N/A"
    total_tokens = "N/A"

    for msg in reversed(conv.get("messages", [])):
        if msg.get("role") == "assistant" and msg.get("council"):
            c = msg.get("council", {})
            meta = c.get("metadata", {})
            verdict = c.get("verdict", {})
            chairman = verdict.get("model") or meta.get("chairman") or chairman
            non_reporting = _extract_non_reporting_models(c, meta)
            raw_members = meta.get("members", []) or [p.get("model") for p in c.get("positions", [])]
            active_members = [
                (m if isinstance(m, str) else m.get("model"))
                for m in raw_members
                if (m if isinstance(m, str) else m.get("model")) not in non_reporting
            ]
            if active_members:
                members_count = str(len(active_members))
            elif raw_members:
                members_count = str(len(raw_members))
            if meta.get("total_tokens"):
                total_tokens = f"{meta['total_tokens']:,}"
            if verdict.get("sections", {}).get("confidence"):
                confidence = verdict["sections"]["confidence"]
            break

    md_content = format_conversation_markdown(conv, mode=mode)
    parser = markdown_it.MarkdownIt().enable("table")
    body_html = parser.render(md_content)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Council Report</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 16mm 16mm 18mm 16mm;
      @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 8pt;
        color: #64748b;
      }}
      @bottom-left {{
        content: "Free LLM Council - Deliberation ID: {conv_id[:8]}";
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 8pt;
        color: #64748b;
      }}
    }}
    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.55;
      color: #0f172a;
      background: #ffffff;
      margin: 0;
      padding: 24px 32px;
    }}
    @media print {{
      body {{
        padding: 0;
      }}
    }}
    .report-banner {{
      border-bottom: 2px solid #0f172a;
      padding-bottom: 14px;
      margin-bottom: 20px;
    }}
    .report-badge {{
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
    }}
    .report-title {{
      font-size: 1.65rem;
      font-weight: 700;
      margin: 0 0 6px 0;
      color: #0f172a;
      line-height: 1.25;
    }}
    .report-subtitle {{
      font-size: 0.95rem;
      color: #475569;
      margin: 0;
    }}
    .report-kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 12px 14px;
      margin-bottom: 24px;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    .kpi-item {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .kpi-label {{
      font-size: 7.5pt;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #64748b;
      font-weight: 600;
    }}
    .kpi-value {{
      font-size: 9.5pt;
      font-weight: 600;
      color: #0f172a;
      word-break: break-word;
    }}
    h1, h2, h3, h4 {{
      color: #0f172a;
      page-break-after: avoid;
      break-after: avoid;
    }}
    h1 {{
      font-size: 1.45rem;
      border-bottom: 1.5px solid #cbd5e1;
      padding-bottom: 4px;
      margin-top: 24px;
      margin-bottom: 12px;
    }}
    h2 {{
      font-size: 1.2rem;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 4px;
      margin-top: 20px;
      margin-bottom: 10px;
    }}
    h3 {{
      font-size: 1.05rem;
      margin-top: 16px;
      margin-bottom: 8px;
    }}
    p, ul, ol {{
      margin: 0.45rem 0;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 9pt;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    th {{
      background: #1e293b !important;
      color: #ffffff !important;
      font-weight: 600;
      text-align: left;
      padding: 8px 10px;
      border: 1px solid #1e293b;
    }}
    td {{
      padding: 7px 10px;
      border: 1px solid #cbd5e1;
      vertical-align: top;
      color: #334155;
    }}
    tr:nth-child(even) td {{
      background: #f8fafc !important;
    }}
    pre {{
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
    }}
    code {{
      font-family: "Cascadia Code", Consolas, Monaco, "Courier New", monospace;
      font-size: 0.9em;
      background: #f1f5f9;
      padding: 2px 4px;
      border-radius: 3px;
    }}
    pre code {{
      background: transparent;
      padding: 0;
      border: none;
    }}
    blockquote {{
      border-left: 4px solid #3b82f6;
      background: #eff6ff;
      margin: 10px 0;
      padding: 8px 12px;
      color: #1e3a8a;
      border-radius: 0 4px 4px 0;
    }}
    hr {{
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 18px 0;
    }}
    .report-footer {{
      margin-top: 36px;
      padding-top: 12px;
      border-top: 1px solid #e2e8f0;
      font-size: 8pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
  </style>
</head>
<body>
  <div class="report-banner">
    <div class="report-badge">Free LLM Council Deliberation Report</div>
    <h1 class="report-title">{title}</h1>
    <p class="report-subtitle">{mode_title}</p>
  </div>

  <div class="report-kpi-grid">
    <div class="kpi-item">
      <span class="kpi-label">Deliberation ID</span>
      <span class="kpi-value">{conv_id[:8]}...</span>
    </div>
    <div class="kpi-item">
      <span class="kpi-label">Created Date</span>
      <span class="kpi-value">{created_at[:10] if created_at else "N/A"}</span>
    </div>
    <div class="kpi-item">
      <span class="kpi-label">Chairman Model</span>
      <span class="kpi-value">{chairman}</span>
    </div>
    <div class="kpi-item">
      <span class="kpi-label">Council Size</span>
      <span class="kpi-value">{members_count} Models</span>
    </div>
    <div class="kpi-item">
      <span class="kpi-label">Confidence Rating</span>
      <span class="kpi-value">{confidence}</span>
    </div>
    <div class="kpi-item">
      <span class="kpi-label">Tokens Consumed</span>
      <span class="kpi-value">{total_tokens}</span>
    </div>
  </div>

  <div class="report-content">
    {body_html}
  </div>

  <div class="report-footer">
    <span>Free LLM Council Multi-Model Deliberation Architecture</span>
    <span>Autonomous Consensus Engine - All Rights Reserved</span>
  </div>
</body>
</html>"""


def generate_report_pdf(conv: Dict[str, Any], mode: str = "executive") -> Optional[bytes]:
    """
    Generate a publication-grade PDF document using an available headless browser.
    Returns bytes on success, or None if no headless browser engine is found.
    """
    browser_bin = find_headless_browser()
    if not browser_bin:
        return None

    html_str = render_report_html(conv, mode=mode)
    with tempfile.TemporaryDirectory() as tmpdir:
        html_file = os.path.join(tmpdir, "report.html")
        pdf_file = os.path.join(tmpdir, "report.pdf")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_str)

        file_uri = "file:///" + os.path.abspath(html_file).replace("\\", "/")
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            file_uri,
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=35)
            if proc.returncode == 0 and os.path.exists(pdf_file):
                with open(pdf_file, "rb") as f:
                    return f.read()
        except Exception:
            return None

    return None



