from unittest.mock import Mock

import pytest
from streamlit.errors import StreamlitSecretNotFoundError

from src.llm import llm_client


@pytest.fixture
def credentials(monkeypatch):
    monkeypatch.delenv("XKIRO_API_KEY", raising=False)
    monkeypatch.setattr(llm_client, "dotenv_values", lambda path: {})
    secrets = Mock()
    secrets.get.side_effect = StreamlitSecretNotFoundError("No secrets found")
    monkeypatch.setattr(llm_client.st, "secrets", secrets)
    return secrets


def test_missing_secrets_gives_setup_message_before_client_creation(credentials, monkeypatch):
    client = Mock()
    monkeypatch.setattr(llm_client, "OpenAI", client)
    with pytest.raises(llm_client.MissingAPIKeyError, match="XKIRO_API_KEY"):
        llm_client.XKiroQwenProvider()
    client.assert_not_called()


def test_environment_key_does_not_require_secrets(credentials, monkeypatch):
    monkeypatch.setenv("XKIRO_API_KEY", "test-environment-key")
    assert llm_client.resolve_api_key() == "test-environment-key"
    credentials.get.assert_not_called()


def test_local_env_key_works_without_secrets(credentials, monkeypatch):
    monkeypatch.setattr(llm_client, "dotenv_values", lambda path: {"XKIRO_API_KEY": "test-local-key"})
    assert llm_client.resolve_api_key() == "test-local-key"
    credentials.get.assert_not_called()


def test_secrets_key_is_supported(credentials):
    credentials.get.side_effect = None
    credentials.get.return_value = "test-secrets-key"
    assert llm_client.resolve_api_key() == "test-secrets-key"


def test_placeholder_key_is_rejected(credentials):
    with pytest.raises(llm_client.MissingAPIKeyError):
        llm_client.resolve_api_key("replace-with-your-xkiro-api-key")
