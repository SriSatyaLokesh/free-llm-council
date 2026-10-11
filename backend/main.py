"""FastAPI backend for LLM Council."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, Response
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
import json
import asyncio
import os

from contextlib import asynccontextmanager
from . import storage
from . import caveman
from . import provider_keys
from . import settings
from .council import run_full_council, generate_conversation_title
from .config import DEBATE_ROUNDS
from .hybrid_client import list_unified_models
from .opencode_client import (
    OpencodeUnavailable,
    default_chairman,
    diagnose_connection,
    ensure_opencode_running,
    list_models,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hook: automatically starts and verifies OpenCode service on server boot."""
    try:
        ensure_opencode_running()
    except Exception as exc:
        print(f"[!] Notice: OpenCode auto-start check returned: {exc}")
    yield

app = FastAPI(title="LLM Council API", lifespan=lifespan)

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    """Convert validation and path traversal ValueErrors to clean HTTP 400 responses."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateConversationRequest(BaseModel):
    """Request to create a new conversation."""
    project_id: Optional[str] = None


class CreateProjectRequest(BaseModel):
    """Request to create a new project workspace folder."""
    name: str
    description: Optional[str] = ""


class UpdateProjectRequest(BaseModel):
    """Request to update a project."""
    name: Optional[str] = None
    description: Optional[str] = None


class UpdateConversationRequest(BaseModel):
    """Request to update a conversation (project assignment, title, or archive status)."""
    title: Optional[str] = None
    project_id: Optional[str] = None
    unlink_project: Optional[bool] = False
    archived: Optional[bool] = None


class SendMessageRequest(BaseModel):
    """Request to send a message in a conversation."""
    content: str
    members: Optional[List[str]] = None
    chairman: Optional[str] = None
    rounds: Optional[int] = None
    token_cap_per_model: Optional[int] = None
    token_budget_total: Optional[int] = None
    time_limit_seconds: Optional[float] = None
    model_thinking: Optional[Dict[str, str]] = None


class SteerRequest(BaseModel):
    """Request to inject human operator guidance into an ongoing debate."""
    message: str
    resources: Optional[List[str]] = None


class SettingsUpdate(BaseModel):
    """Live settings the user can change while a run is in flight."""
    debateMode: Optional[str] = None
    tokenCapPerModel: Optional[int] = None
    tokenBudgetTotal: Optional[int] = None
    timeLimitSeconds: Optional[float] = None



class ConversationMetadata(BaseModel):
    """Conversation metadata for list view."""
    id: str
    created_at: str
    title: str
    message_count: int
    project_id: Optional[str] = None
    archived: bool = False


class Conversation(BaseModel):
    """Full conversation with all messages."""
    id: str
    created_at: str
    title: str
    messages: List[Dict[str, Any]]
    project_id: Optional[str] = None
    archived: bool = False


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "LLM Council API"}


@app.get("/api/health")
async def health():
    """Detailed health check validating connection to OpenCode and BYOK readiness."""
    diagnosis = await diagnose_connection()
    is_opencode_connected = diagnosis.get("status") == "connected"
    any_byok_keys = any(s.get("configured") for s in provider_keys.get_key_statuses().values())

    mode = "hybrid" if (is_opencode_connected and any_byok_keys) else "opencode" if is_opencode_connected else "byok" if any_byok_keys else "setup"
    is_ok = is_opencode_connected or any_byok_keys

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok" if is_ok else "setup",
            "mode": mode,
            "opencode": diagnosis,
        },
    )



class ProviderKeyUpdate(BaseModel):
    """Payload to configure or remove a provider API key."""
    provider: str
    key: Optional[str] = None


@app.get("/api/providers/keys")
async def get_provider_keys():
    """Get status and redacted preview of configured provider API keys."""
    return provider_keys.get_key_statuses()


@app.post("/api/providers/keys")
async def post_provider_key(request: ProviderKeyUpdate):
    """Update or remove a provider API key dynamically."""
    provider_keys.set_key(request.provider, request.key)
    return provider_keys.get_key_statuses()


@app.get("/api/models")
async def get_models():
    """
    The council roster, read live from OpenCode and configured custom providers.
    Supports running purely with BYOK keys when OpenCode daemon is offline.
    """
    try:
        models = await list_unified_models()
    except Exception as exc:
        print(f"[models] Error listing models: {exc}")
        models = []

    try:
        chairman = await default_chairman(models)
    except Exception:
        chairman = None

    return {
        "models": models,
        "defaultChairman": chairman,
        "defaultRounds": DEBATE_ROUNDS,
    }


@app.get("/api/settings")
async def get_settings():
    """
    Current council settings, plus whether the official Caveman skill is
    installed. The mode is process-global so it can be flipped mid-run.
    """
    return {**settings.get_settings(), "caveman": caveman.status()}


@app.post("/api/settings")
async def post_settings(request: SettingsUpdate):
    """Change live council settings. Takes effect on the next debate round."""
    if request.debateMode is not None and request.debateMode not in settings.DEBATE_MODES:
        raise HTTPException(
            status_code=400,
            detail=f"debateMode must be one of {list(settings.DEBATE_MODES)}",
        )
    patch = {}
    if request.debateMode is not None:
        patch["debateMode"] = request.debateMode
    if request.tokenCapPerModel is not None:
        patch["tokenCapPerModel"] = request.tokenCapPerModel
    if request.tokenBudgetTotal is not None:
        patch["tokenBudgetTotal"] = request.tokenBudgetTotal
    if request.timeLimitSeconds is not None:
        patch["timeLimitSeconds"] = request.timeLimitSeconds

    updated = settings.update_settings(patch)
    return {**updated, "caveman": caveman.status()}



@app.get("/api/projects")
async def list_projects():
    """List all project folders with metadata and debate counts."""
    return storage.list_projects()


@app.post("/api/projects")
async def create_project(request: CreateProjectRequest):
    """Create a new project workspace folder."""
    if not request.name.strip():
        raise HTTPException(status_code=400, detail="Project name cannot be empty")
    return storage.create_project(name=request.name.strip(), description=request.description or "")


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get details for a specific project."""
    proj = storage.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@app.patch("/api/projects/{project_id}")
async def update_project(project_id: str, request: UpdateProjectRequest):
    """Update a project name or description."""
    proj = storage.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    patch = {}
    if request.name is not None:
        if not request.name.strip():
            raise HTTPException(status_code=400, detail="Project name cannot be empty")
        patch["name"] = request.name.strip()
    if request.description is not None:
        patch["description"] = request.description
    updated = storage.update_project(project_id, patch)
    return updated


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project folder and revert its debates to independent mode."""
    deleted = storage.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "ok", "deleted": project_id}


@app.get("/api/conversations", response_model=List[ConversationMetadata])
async def list_conversations():
    """List all conversations (metadata only)."""
    return storage.list_conversations()


@app.post("/api/conversations", response_model=Conversation)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation."""
    conversation_id = str(uuid.uuid4())
    conversation = storage.create_conversation(conversation_id, project_id=request.project_id)
    return conversation


@app.get("/api/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all its messages."""
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@app.patch("/api/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(conversation_id: str, request: UpdateConversationRequest):
    """Update conversation metadata such as title or assigned project folder."""
    conv = storage.get_conversation(conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if request.title is not None:
        storage.update_conversation_title(conversation_id, request.title)

    if request.archived is not None:
        storage.set_conversation_archived(conversation_id, request.archived)

    if request.unlink_project or request.project_id == "":
        storage.assign_conversation_project(conversation_id, None)
    elif request.project_id is not None:
        proj = storage.get_project(request.project_id)
        if not proj:
            raise HTTPException(status_code=404, detail="Project not found")
        storage.assign_conversation_project(conversation_id, request.project_id)

    updated = storage.get_conversation(conversation_id)
    return updated


@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation by ID."""
    deleted = storage.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "ok", "deleted": conversation_id}


@app.post("/api/conversations/prune-empty")
async def prune_empty_conversations():
    """Prune all empty abandoned conversations (0 messages)."""
    count = storage.prune_empty_conversations()
    return {"status": "ok", "pruned_count": count}


@app.get("/api/conversations/{conversation_id}/export/report")
async def export_conversation_report(
    conversation_id: str,
    format: str = Query("executive", description="Report format: 'executive' or 'detailed'"),
):
    """Export a council deliberation as a formatted Markdown report document (executive or detailed)."""
    conv = storage.get_conversation(conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    md_content = storage.format_conversation_markdown(conv, mode=format)
    fmt_tag = "detailed" if format in ("detailed", "comprehensive") else "executive"
    filename = f"council-{fmt_tag}-report-{conversation_id[:8]}.md"
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache",
        },
    )


@app.get("/api/conversations/{conversation_id}/export/html")
async def export_conversation_html(
    conversation_id: str,
    format: str = Query("executive", description="Report format: 'executive' or 'detailed'"),
):
    """Export a council deliberation as a standalone publication-grade HTML report."""
    conv = storage.get_conversation(conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    html_content = storage.render_report_html(conv, mode=format)
    fmt_tag = "detailed" if format in ("detailed", "comprehensive") else "executive"
    filename = f"council-{fmt_tag}-report-{conversation_id[:8]}.html"
    return Response(
        content=html_content,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache",
        },
    )


@app.get("/api/conversations/{conversation_id}/export/pdf")
async def export_conversation_pdf(
    conversation_id: str,
    format: str = Query("executive", description="Report format: 'executive' or 'detailed'"),
):
    """Export a council deliberation as a publication-grade PDF document."""
    conv = storage.get_conversation(conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    pdf_bytes = storage.generate_report_pdf(conv, mode=format)
    if not pdf_bytes:
        raise HTTPException(
            status_code=501,
            detail="Headless browser engine (Edge/Chrome/Chromium) is not available on host for PDF rendering. Please use the Print/PDF export in the web viewer or download the HTML report.",
        )

    fmt_tag = "detailed" if format in ("detailed", "comprehensive") else "executive"
    filename = f"council-{fmt_tag}-report-{conversation_id[:8]}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache",
        },
    )


@app.get("/api/conversations/{conversation_id}/reports")
async def get_conversation_reports(conversation_id: str):
    """
    Return pre-rendered executive and detailed reports with deliberation metadata
    for the interactive in-app Report Viewer.
    """
    conv = storage.get_conversation(conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    executive_md = storage.format_conversation_executive(conv)
    detailed_md = storage.format_conversation_detailed(conv)

    return {
        "id": conversation_id,
        "title": conv.get("title", "Council Deliberation"),
        "created_at": conv.get("created_at"),
        "executive_report": executive_md,
        "detailed_report": detailed_md,
    }


@app.get("/api/conversations/{conversation_id}/export/zip")
async def export_conversation_zip_archive(conversation_id: str):
    """Export the entire council discussion as a downloadable ZIP package containing report.md, conversation.json, and summary.txt."""
    conv = storage.get_conversation(conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    zip_bytes = storage.export_conversation_zip(conv)
    filename = f"council-deliberation-{conversation_id[:8]}.zip"
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache",
        },
    )


@app.post("/api/conversations/{conversation_id}/message")
async def send_message(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and run the full four-stage council.

    Returns the complete response with every stage.
    """
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    is_first_message = len(conversation["messages"]) == 0

    storage.add_user_message(conversation_id, request.content)

    if is_first_message:
        title = await generate_conversation_title(request.content)
        storage.update_conversation_title(conversation_id, title)

    try:
        result = await run_full_council(
            request.content,
            members=request.members,
            chairman=request.chairman,
            rounds=request.rounds,
            token_cap_per_model=request.token_cap_per_model
            if request.token_cap_per_model is not None
            else settings.get_token_cap_per_model(),
            token_budget_total=request.token_budget_total
            if request.token_budget_total is not None
            else settings.get_token_budget_total(),
            time_limit_seconds=request.time_limit_seconds
            if request.time_limit_seconds is not None
            else settings.get_time_limit_seconds(),
            model_thinking=request.model_thinking,
        )
    except OpencodeUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    storage.add_assistant_message(conversation_id, result)

    return result


@app.post("/api/conversations/{conversation_id}/steer")
async def steer_conversation(conversation_id: str, request: SteerRequest):
    """Inject human operator guidance and resources into an ongoing deliberation."""
    from .council import get_active_run
    run = get_active_run(conversation_id)
    if not run:
        raise HTTPException(
            status_code=400,
            detail="No active council run found for this conversation to steer.",
        )
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Steering message cannot be empty")
    entry = run.inject_steering(request.message, request.resources)
    return {"status": "ok", "steering": entry}


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and stream the council as it runs.

    Emits Server-Sent Events as each stage completes, so the UI can fill in
    progressively instead of waiting for the whole deliberation.
    """
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    is_first_message = len(conversation["messages"]) == 0

    def emit(event_type: str, **payload) -> str:
        return f"data: {json.dumps({'type': event_type, **payload})}\n\n"

    async def event_generator():
        from .council import (
            CouncilRun,
            resolve_roster,
            register_active_run,
            unregister_active_run,
        )

        run = None
        try:
            storage.add_user_message(conversation_id, request.content)

            title_task = None
            if is_first_message:
                title_task = asyncio.create_task(
                    generate_conversation_title(request.content)
                )

            try:
                members, chairman = await resolve_roster(
                    request.members, request.chairman
                )
            except Exception as exc:
                yield emit("error", message=f"Could not assemble the council: {exc}")
                return

            run = CouncilRun(
                request.content,
                members,
                chairman,
                request.rounds,
                token_cap_per_model=request.token_cap_per_model
                if request.token_cap_per_model is not None
                else settings.get_token_cap_per_model(),
                token_budget_total=request.token_budget_total
                if request.token_budget_total is not None
                else settings.get_token_budget_total(),
                time_limit_seconds=request.time_limit_seconds
                if request.time_limit_seconds is not None
                else settings.get_time_limit_seconds(),
                model_thinking=request.model_thinking,
            )
            register_active_run(conversation_id, run)

            queue: asyncio.Queue = asyncio.Queue()

            async def drive():
                """Run the pipeline, pushing stage results onto the queue.

                `run_stream` always terminates the queue with a (None, None)
                sentinel, so this wrapper adds nothing to the protocol.
                """
                await run.run_stream(queue)

            task = asyncio.create_task(drive())

            stage_keys = {
                "positions": "positions",
                "debate_round": "debate",
                "review": "review",
                "verdict": "verdict",
            }

            while True:
                kind, payload = await queue.get()
                if kind is None:
                    break
                if kind in stage_keys:
                    yield emit(f"{kind}_complete", data=payload)
                elif kind == "roster":
                    yield emit("roster", data=payload)
                elif kind == "aggregate":
                    yield emit("aggregate_complete", data=payload)
                elif kind == "model_evicted":
                    yield emit("model_evicted", data=payload)
                elif kind == "model_retired":
                    yield emit("model_retired", data=payload)
                elif kind == "debate_concluded_early":
                    yield emit("debate_concluded_early", data=payload)
                elif kind == "human_guidance_injected":
                    yield emit("human_guidance_injected", data=payload)
                elif kind == "error":
                    yield emit("error", message=payload.get("message"))

            await task

            if title_task:
                title = await title_task
                storage.update_conversation_title(conversation_id, title)
                yield emit("title_complete", data={"title": title})

            # Persist once the run is finished.
            last = storage.get_conversation(conversation_id)
            if last and last["messages"] and last["messages"][-1]["role"] == "user":
                result = getattr(run, "result", None)
                if result:
                    storage.add_assistant_message(conversation_id, result)
                    yield emit("persisted")

            yield emit("complete")

        except Exception as exc:
            yield emit("error", message=str(exc))
        finally:
            unregister_active_run(conversation_id)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


if __name__ == "__main__":
    import uvicorn
    ensure_opencode_running()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host=host, port=port)
