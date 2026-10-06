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

def format_conversation_markdown(conv: Dict[str, Any]) -> str:
    """
    Format a complete council deliberation into a clean, comprehensive Markdown report.
    """
    title = conv.get("title", "Council Deliberation")
    conv_id = conv.get("id", "unknown")
    created = conv.get("created_at", "")
    lines = [
        f"# {title}",
        f"",
        f"- **Deliberation ID:** `{conv_id}`",
        f"- **Date & Time:** {created}",
        f"",
        "---",
        "",
    ]

    messages = conv.get("messages", [])
    if not messages:
        lines.append("*No messages recorded in this council session.*")
        return "\n".join(lines)

    for idx, msg in enumerate(messages):
        role = msg.get("role", "unknown")
        if role == "user":
            lines.extend([
                f"## Query / Prompt",
                f"",
                msg.get("content", "").strip(),
                f"",
                "---",
                "",
            ])
        elif role == "assistant":
            council = msg.get("council", {})
            metadata = council.get("metadata", {}) or msg.get("metadata", {})

            # 1. Chairman Verdict
            verdict = council.get("verdict", {})
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
                                f"",
                                f"### {sec_title}",
                                f"",
                                sections[sec_key].strip(),
                            ])
                elif verdict.get("response"):
                    lines.extend([
                        f"",
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


def export_conversation_zip(conv: Dict[str, Any]) -> bytes:
    """
    Build an in-memory zip archive containing:
      - report.md (human-readable comprehensive report)
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

        # 2. Comprehensive Markdown report
        markdown_report = format_conversation_markdown(conv)
        zf.writestr("report.md", markdown_report.encode("utf-8"))

        # 3. Concise summary
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

