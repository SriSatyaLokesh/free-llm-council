"""Unit and integration tests for Phase 10: Projects & Workspace Folder Hierarchy."""

import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend import storage


def test_project_storage_crud():
    """Verify backend storage CRUD operations for projects."""
    # 1. Create project
    proj = storage.create_project(name="Core Architecture", description="Deep dive discussions")
    assert proj is not None
    assert "id" in proj
    assert proj["name"] == "Core Architecture"
    assert proj["description"] == "Deep dive discussions"
    proj_id = proj["id"]

    # 2. Get project
    fetched = storage.get_project(proj_id)
    assert fetched is not None
    assert fetched["id"] == proj_id

    # 3. Update project
    updated = storage.update_project(proj_id, {"name": "Core Architecture V2"})
    assert updated is not None
    assert updated["name"] == "Core Architecture V2"

    # 4. List projects
    projs = storage.list_projects()
    assert any(p["id"] == proj_id for p in projs)

    # 5. Delete project
    deleted = storage.delete_project(proj_id)
    assert deleted is True
    assert storage.get_project(proj_id) is None


def test_conversation_project_assignment_and_unlinking():
    """Verify linking a debate to a project and unlinking when project is deleted."""
    # Create project and conversation
    proj = storage.create_project(name="Cache Project")
    proj_id = proj["id"]

    conv_id = "test_conv_for_project"
    storage.create_conversation(conv_id)
    storage.add_user_message(conv_id, "Which cache to use?")

    # Initially independent (project_id is None)
    conv = storage.get_conversation(conv_id)
    assert conv.get("project_id") is None

    # Assign to project
    success = storage.assign_conversation_project(conv_id, proj_id)
    assert success is True

    conv_after = storage.get_conversation(conv_id)
    assert conv_after.get("project_id") == proj_id

    # Check project conversation count in list_projects
    projs = storage.list_projects()
    proj_meta = next(p for p in projs if p["id"] == proj_id)
    assert proj_meta.get("conversation_count") == 1

    # Delete project -> conversation should revert to independent (project_id is None)
    storage.delete_project(proj_id)
    conv_reverted = storage.get_conversation(conv_id)
    assert conv_reverted is not None
    assert conv_reverted.get("project_id") is None

    # Clean up
    storage.delete_conversation(conv_id)


@pytest.mark.asyncio
async def test_projects_http_api():
    """HTTP API integration tests for /api/projects and /api/conversations/{id}."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create Project
        res = await client.post("/api/projects", json={"name": "UI Redesign", "description": "Debates on UI"})
        assert res.status_code == 200
        proj_data = res.json()
        proj_id = proj_data["id"]
        assert proj_data["name"] == "UI Redesign"

        # List Projects
        res_list = await client.get("/api/projects")
        assert res_list.status_code == 200
        projects = res_list.json()
        assert any(p["id"] == proj_id for p in projects)

        # Create Conversation
        res_conv = await client.post("/api/conversations", json={})
        assert res_conv.status_code == 200
        conv_id = res_conv.json()["id"]

        # Assign Conversation to Project
        res_patch = await client.patch(f"/api/conversations/{conv_id}", json={"project_id": proj_id})
        assert res_patch.status_code == 200
        assert res_patch.json().get("project_id") == proj_id

        # Update Project Name
        res_proj_patch = await client.patch(f"/api/projects/{proj_id}", json={"name": "UI Redesign 2026"})
        assert res_proj_patch.status_code == 200
        assert res_proj_patch.json().get("name") == "UI Redesign 2026"

        # Delete Project
        res_del = await client.delete(f"/api/projects/{proj_id}")
        assert res_del.status_code == 200

        # Clean up conversation
        await client.delete(f"/api/conversations/{conv_id}")


@pytest.mark.asyncio
async def test_create_conversation_with_project_and_move_lifecycle():
    """Verify creating debate directly in project, moving between projects, and unlinking."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create two projects
        p1 = (await client.post("/api/projects", json={"name": "Folder Alpha"})).json()
        p2 = (await client.post("/api/projects", json={"name": "Folder Beta"})).json()
        p1_id, p2_id = p1["id"], p2["id"]

        # 2. Create conversation directly scoped to Folder Alpha
        c_res = await client.post("/api/conversations", json={"project_id": p1_id})
        assert c_res.status_code == 200
        conv = c_res.json()
        conv_id = conv["id"]
        assert conv["project_id"] == p1_id

        # 3. Get conversation verifies assignment
        get_res = await client.get(f"/api/conversations/{conv_id}")
        assert get_res.status_code == 200
        assert get_res.json()["project_id"] == p1_id

        # 4. Move conversation to Folder Beta
        move_res = await client.patch(f"/api/conversations/{conv_id}", json={"project_id": p2_id})
        assert move_res.status_code == 200
        assert move_res.json()["project_id"] == p2_id

        # 5. Move conversation to Independent Standalone
        unlink_res = await client.patch(f"/api/conversations/{conv_id}", json={"unlink_project": True})
        assert unlink_res.status_code == 200
        assert unlink_res.json().get("project_id") is None

        # Clean up
        await client.delete(f"/api/conversations/{conv_id}")
        await client.delete(f"/api/projects/{p1_id}")
        await client.delete(f"/api/projects/{p2_id}")


def test_conversation_archive_and_rename_storage():
    """Verify backend storage archiving and renaming functionality."""
    conv_id = "test_conv_archive_rename"
    storage.create_conversation(conv_id)
    storage.add_user_message(conv_id, "Debate question")

    # By default, archived is False
    conv = storage.get_conversation(conv_id)
    assert conv.get("archived") is False

    # Rename conversation
    storage.update_conversation_title(conv_id, "Renamed Debate Title")
    conv_renamed = storage.get_conversation(conv_id)
    assert conv_renamed.get("title") == "Renamed Debate Title"

    # Archive conversation
    storage.set_conversation_archived(conv_id, True)
    conv_archived = storage.get_conversation(conv_id)
    assert conv_archived.get("archived") is True

    # List conversations should reflect archived flag
    convs = storage.list_conversations()
    found = next((c for c in convs if c["id"] == conv_id), None)
    assert found is not None
    assert found["archived"] is True
    assert found["title"] == "Renamed Debate Title"

    # Restore / unarchive conversation
    storage.set_conversation_archived(conv_id, False)
    conv_unarchived = storage.get_conversation(conv_id)
    assert conv_unarchived.get("archived") is False

    # Clean up
    storage.delete_conversation(conv_id)


@pytest.mark.asyncio
async def test_conversation_archive_and_rename_api():
    """Verify HTTP API PATCH endpoint for renaming and archiving conversations."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create conversation
        res = await client.post("/api/conversations", json={})
        assert res.status_code == 200
        conv_id = res.json()["id"]

        # Add message so it's not filtered out as empty
        storage.add_user_message(conv_id, "Hello council")

        # Rename conversation
        res_rename = await client.patch(f"/api/conversations/{conv_id}", json={"title": "Custom Title 123"})
        assert res_rename.status_code == 200
        assert res_rename.json()["title"] == "Custom Title 123"

        # Archive conversation
        res_archive = await client.patch(f"/api/conversations/{conv_id}", json={"archived": True})
        assert res_archive.status_code == 200
        assert res_archive.json()["archived"] is True

        # Verify in conversation list
        res_list = await client.get("/api/conversations")
        assert res_list.status_code == 200
        conv_meta = next(c for c in res_list.json() if c["id"] == conv_id)
        assert conv_meta["archived"] is True
        assert conv_meta["title"] == "Custom Title 123"

        # Restore conversation
        res_restore = await client.patch(f"/api/conversations/{conv_id}", json={"archived": False})
        assert res_restore.status_code == 200
        assert res_restore.json()["archived"] is False

        # Clean up
        await client.delete(f"/api/conversations/{conv_id}")

