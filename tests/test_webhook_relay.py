"""Signature-verification tests for the Sovereign Edge webhook relay.

The relay triggers an autonomous GitOps loop, so authenticating the sender is a
Diamond-tier security gate. These tests are skipped if the webhook extras
(FastAPI / swarm graph) are not installed in the current environment.
"""

import hashlib
import hmac
import importlib
import os
import sys

import pytest

# The webhook relay lives at the repo root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

pytest.importorskip("fastapi", reason="webhook extras not installed")

try:
    webhook_relay = importlib.import_module("webhook_relay")
except ImportError as exc:  # optional webhook deps (fastapi, swarm graph, langgraph, …)
    pytest.skip(f"webhook_relay not importable: {exc}", allow_module_level=True)


def _sign(secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()


def test_rejects_when_secret_unset(monkeypatch):
    # Fail-closed: an empty configured secret must reject everything, even a
    # signature an attacker computed against the empty key.
    monkeypatch.setattr(webhook_relay, "WEBHOOK_SECRET", "")
    body = b'{"action":"opened"}'
    forged = _sign("", body)
    assert webhook_relay.verify_github_signature(body, forged) is False


def test_rejects_bad_signature(monkeypatch):
    monkeypatch.setattr(webhook_relay, "WEBHOOK_SECRET", "s3cr3t")
    body = b'{"action":"opened"}'
    assert webhook_relay.verify_github_signature(body, "sha256=deadbeef") is False


def test_rejects_missing_header(monkeypatch):
    monkeypatch.setattr(webhook_relay, "WEBHOOK_SECRET", "s3cr3t")
    assert webhook_relay.verify_github_signature(b"{}", "") is False


def test_accepts_valid_signature(monkeypatch):
    secret = "s3cr3t"
    monkeypatch.setattr(webhook_relay, "WEBHOOK_SECRET", secret)
    body = b'{"action":"opened"}'
    assert webhook_relay.verify_github_signature(body, _sign(secret, body)) is True
