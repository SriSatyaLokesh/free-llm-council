"""Unit tests for Phase 9: Clean Conversation Lifecycle & Persisted Council Presets."""

import pytest
from unittest.mock import patch
from backend import storage


def test_delete_conversation():
    """Verify that a conversation can be permanently deleted from storage."""
    conv_id = "test_conv_to_delete"
    storage.create_conversation(conv_id)
    assert storage.get_conversation(conv_id) is not None

    deleted = storage.delete_conversation(conv_id)
    assert deleted is True
    assert storage.get_conversation(conv_id) is None

    # Deleting non-existent returns False
    assert storage.delete_conversation("non_existent_id") is False


def test_prune_empty_conversations():
    """Verify that abandoned empty conversations (0 messages) are pruned."""
    empty_1 = "test_empty_1"
    empty_2 = "test_empty_2"
    with_msg = "test_with_msg"

    storage.create_conversation(empty_1)
    storage.create_conversation(empty_2)
    storage.create_conversation(with_msg)
    storage.add_user_message(with_msg, "Hello council!")

    pruned_count = storage.prune_empty_conversations(except_id=None)
    assert pruned_count >= 2

    assert storage.get_conversation(empty_1) is None
    assert storage.get_conversation(empty_2) is None
    assert storage.get_conversation(with_msg) is not None

    # Clean up
    storage.delete_conversation(with_msg)


def test_list_conversations_excludes_empty():
    """Verify list_conversations does not return phantom empty conversations."""
    empty_id = "test_phantom_empty"
    valid_id = "test_valid_conv"

    storage.create_conversation(empty_id)
    storage.create_conversation(valid_id)
    storage.add_user_message(valid_id, "Analyze architecture")

    convs = storage.list_conversations()
    conv_ids = [c["id"] for c in convs]

    assert valid_id in conv_ids
    assert empty_id not in conv_ids

    # Clean up
    storage.delete_conversation(empty_id)
    storage.delete_conversation(valid_id)


def test_preset_auto_reconciliation():
    """
    Verify preset reconciliation logic:
    If a saved model is missing from OpenCode, reconcile with updated version
    or available models while keeping valid settings intact.
    """
    from backend.settings import reconcile_council_preset

    saved_preset = {
        "members": ["opencode/ling-3.0-flash-fin-free", "opencode/space-bunny-free"],
        "chairman": "opencode/ling-3.0-flash-fin-free",
        "rounds": 3,
        "debateMode": "full",
        "tokenCapPerModel": 10000,
        "modelThinking": {
            "opencode/ling-3.0-flash-fin-free": "high",
            "opencode/space-bunny-free": "max",
        },
    }

    # Live OpenCode models: ling-3.0 is gone, ling-3.1 is available, space-bunny is available, big-pickle is available
    available_models = [
        {"id": "opencode/ling-3.1-flash-free", "name": "Ling 3.1 Flash Free"},
        {"id": "opencode/space-bunny-free", "name": "Space Bunny Free"},
        {"id": "opencode/big-pickle", "name": "Big Pickle"},
    ]

    reconciled = reconcile_council_preset(saved_preset, available_models)

    # Must preserve valid members
    assert "opencode/space-bunny-free" in reconciled["members"]
    # ling-3.0 should update to ling-3.1
    assert "opencode/ling-3.1-flash-free" in reconciled["members"]
    assert "opencode/ling-3.0-flash-fin-free" not in reconciled["members"]

    # Chairman should update to ling-3.1 or valid model
    assert reconciled["chairman"] in ["opencode/ling-3.1-flash-free", "opencode/space-bunny-free"]

    # Unaltered config preserved
    assert reconciled["rounds"] == 3
    assert reconciled["debateMode"] == "full"
    assert reconciled["tokenCapPerModel"] == 10000
