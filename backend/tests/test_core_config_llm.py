"""
Unit tests for `backend.app.core.config` and `backend.app.core.llm`.
"""
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from backend.app.core.config import Settings, get_settings
from backend.app.core.llm import (
    AnthropicProvider,
    ChatMessage,
    GeminiProvider,
    LLMConfigurationError,
    LLMProviderError,
    LLMRateLimitError,
    LLMTimeoutError,
    OllamaProvider,
    OpenAIProvider,
    create_llm_client,
)


async def _async_iter(items):
    for item in items:
        yield item


def test_settings_defaults_and_env_override(monkeypatch):
    get_settings.cache_clear()
    settings = Settings(_env_file=None)
    assert settings.LLM_PROVIDER == "ollama"
    assert settings.LLM_MODEL == "llama3.2"
    assert settings.REQUIRE_COMMAND_APPROVAL is True

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("LLM_MODEL", "gemini-2.0-flash")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    get_settings.cache_clear()
    overridden = get_settings()
    assert overridden.LLM_PROVIDER == "gemini"
    assert overridden.LLM_MODEL == "gemini-2.0-flash"
    assert overridden.GEMINI_API_KEY == "test-key"
    get_settings.cache_clear()


def test_create_llm_client_requires_api_keys():
    with pytest.raises(LLMConfigurationError, match="GEMINI_API_KEY"):
        create_llm_client(Settings(_env_file=None, LLM_PROVIDER="gemini", GEMINI_API_KEY=None))

    with pytest.raises(LLMConfigurationError, match="OPENAI_API_KEY"):
        create_llm_client(Settings(_env_file=None, LLM_PROVIDER="openai", OPENAI_API_KEY=None))

    with pytest.raises(LLMConfigurationError, match="ANTHROPIC_API_KEY"):
        create_llm_client(Settings(_env_file=None, LLM_PROVIDER="anthropic", ANTHROPIC_API_KEY=None))


def test_create_llm_client_selects_ollama_without_api_key():
    client = create_llm_client(Settings(_env_file=None, LLM_PROVIDER="ollama"))
    assert isinstance(client, OllamaProvider)


@pytest.mark.asyncio
async def test_gemini_provider_generate_stream_and_count_tokens():
    mock_models = SimpleNamespace(
        generate_content=AsyncMock(
            return_value=SimpleNamespace(
                text="Hello from Gemini",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=12,
                    candidates_token_count=5,
                    total_token_count=17,
                ),
                candidates=[SimpleNamespace(finish_reason="STOP")],
            )
        ),
        generate_content_stream=AsyncMock(
            return_value=_async_iter(
                [SimpleNamespace(text="Hello "), SimpleNamespace(text="world")]
            )
        ),
        count_tokens=AsyncMock(return_value=SimpleNamespace(total_tokens=14)),
    )
    mock_client = SimpleNamespace(aio=SimpleNamespace(models=mock_models))
    settings = Settings(
        _env_file=None,
        LLM_PROVIDER="gemini",
        LLM_MODEL="gemini-2.0-flash",
        GEMINI_API_KEY="dummy",
    )
    provider = GeminiProvider(settings, client=mock_client)

    messages = [
        ChatMessage(role="system", content="Be concise."),
        ChatMessage(role="user", content="Hi"),
        ChatMessage(role="assistant", content="Hello!"),
        ChatMessage(role="user", content="How are tokens counted?"),
    ]
    response = await provider.generate(messages, system_prompt="You are JARVIS.")

    assert response.content == "Hello from Gemini"
    assert response.provider == "gemini"
    assert response.model == "gemini-2.0-flash"
    assert response.usage.input_tokens == 12
    assert response.usage.output_tokens == 5
    assert response.usage.total_tokens == 17
    assert response.finish_reason == "STOP"

    call_kwargs = mock_models.generate_content.call_args.kwargs
    assert call_kwargs["config"].system_instruction == "You are JARVIS.\n\nBe concise."
    assert [c.role for c in call_kwargs["contents"]] == ["user", "model", "user"]

    chunks = [chunk async for chunk in provider.stream(messages)]
    assert chunks == ["Hello ", "world"]

    token_count = await provider.count_tokens(messages, system_prompt="You are JARVIS.")
    assert token_count == 14


@pytest.mark.asyncio
async def test_gemini_provider_maps_rate_limit_and_timeout():
    from google.genai import errors as genai_errors

    rate_limit_exc = genai_errors.APIError(
        code=429,
        response_json={"error": {"message": "Too Many Requests"}},
    )
    mock_models = SimpleNamespace(
        generate_content=AsyncMock(side_effect=rate_limit_exc),
    )
    mock_client = SimpleNamespace(aio=SimpleNamespace(models=mock_models))
    provider = GeminiProvider(
        Settings(_env_file=None, LLM_PROVIDER="gemini", GEMINI_API_KEY="dummy"),
        client=mock_client,
    )

    with pytest.raises(LLMRateLimitError) as exc_info:
        await provider.generate([ChatMessage(role="user", content="hi")])
    assert exc_info.value.retryable is True

    mock_models.generate_content.side_effect = TimeoutError("timed out")
    with pytest.raises(LLMTimeoutError) as timeout_info:
        await provider.generate([ChatMessage(role="user", content="hi")])
    assert timeout_info.value.retryable is True


@pytest.mark.asyncio
async def test_ollama_provider_generate_and_stream():
    async def fake_chat(*, model, messages, stream=False, options=None):
        if stream:
            return _async_iter(
                [
                    {"message": {"content": "Local "}},
                    {"message": {"content": "LLM"}},
                ]
            )
        return {
            "message": {"content": "Local response"},
            "prompt_eval_count": 9,
            "eval_count": 4,
            "done_reason": "stop",
        }

    mock_client = SimpleNamespace(chat=AsyncMock(side_effect=fake_chat))
    provider = OllamaProvider(
        Settings(_env_file=None, LLM_PROVIDER="ollama", LLM_MODEL="llama3.2"),
        client=mock_client,
    )

    msgs = [ChatMessage(role="user", content="Hello")]
    resp = await provider.generate(msgs, system_prompt="System rule")
    assert resp.content == "Local response"
    assert resp.usage.input_tokens == 9
    assert resp.usage.output_tokens == 4
    assert resp.usage.total_tokens == 13
    assert resp.finish_reason == "stop"

    chunks = [chunk async for chunk in provider.stream(msgs)]
    assert chunks == ["Local ", "LLM"]

    estimated = await provider.count_tokens(msgs, system_prompt="System rule")
    assert estimated > 0


@pytest.mark.asyncio
async def test_ollama_provider_maps_connect_error():
    import httpx

    mock_client = SimpleNamespace(
        chat=AsyncMock(side_effect=httpx.ConnectError("Connection refused"))
    )
    provider = OllamaProvider(
        Settings(_env_file=None, LLM_PROVIDER="ollama"),
        client=mock_client,
    )
    with pytest.raises(LLMProviderError) as exc_info:
        await provider.generate([ChatMessage(role="user", content="hi")])
    assert exc_info.value.retryable is True


@pytest.mark.asyncio
async def test_openai_and_anthropic_providers_generate():
    openai_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=AsyncMock(
                    return_value=SimpleNamespace(
                        choices=[
                            SimpleNamespace(
                                message=SimpleNamespace(content="OpenAI reply"),
                                finish_reason="stop",
                            )
                        ],
                        usage=SimpleNamespace(
                            prompt_tokens=10,
                            completion_tokens=6,
                            total_tokens=16,
                        ),
                    )
                )
            )
        )
    )
    oa = OpenAIProvider(
        Settings(_env_file=None, LLM_PROVIDER="openai", LLM_MODEL="gpt-4o-mini", OPENAI_API_KEY="k"),
        client=openai_client,
    )
    oa_resp = await oa.generate([ChatMessage(role="user", content="hi")])
    assert oa_resp.content == "OpenAI reply"
    assert oa_resp.usage.total_tokens == 16

    anthropic_client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(
                return_value=SimpleNamespace(
                    content=[SimpleNamespace(type="text", text="Claude reply")],
                    usage=SimpleNamespace(input_tokens=8, output_tokens=7),
                    stop_reason="end_turn",
                )
            )
        )
    )
    ant = AnthropicProvider(
        Settings(
            _env_file=None,
            LLM_PROVIDER="anthropic",
            LLM_MODEL="claude-3-5-sonnet-20241022",
            ANTHROPIC_API_KEY="k",
        ),
        client=anthropic_client,
    )
    ant_resp = await ant.generate([ChatMessage(role="user", content="hi")], system_prompt="sys")
    assert ant_resp.content == "Claude reply"
    assert ant_resp.usage.total_tokens == 15
    assert ant_resp.finish_reason == "end_turn"

