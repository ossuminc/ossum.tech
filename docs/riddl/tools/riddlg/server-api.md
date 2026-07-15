---
title: "Server API"
description: "The HTTP API served by riddlg serve — generation, MCP over HTTP, chat, and model status"
---

# Server API

`riddlg serve` runs a localhost HTTP service exposing riddlg's capabilities to
other programs. It is how [Synapify](../../../synapify/index.md) drives riddlg,
and it is a supported integration point for your own tooling.

```bash
riddlg serve                       # http://127.0.0.1:8910
riddlg serve --host 0.0.0.0 --port 9000 --provider anthropic
```

The server binds `127.0.0.1:8910` by default and locks its
[AI provider](ai-providers.md) at startup — restart to change it, or override
per request on [`/generate/riddl`](#post-generateriddl).

!!! warning "There is no authentication on the server itself"
    The default bind is loopback-only for good reason. Anything that can reach
    the port can use it; only Pro entitlement is checked, never identity. Think
    twice before `--host 0.0.0.0`.

## Endpoints

| Method | Path | Tier | Purpose |
|--------|------|------|---------|
| `GET` | [`/health`](#get-health) | Free | Liveness check |
| `GET` | [`/model/status`](#get-modelstatus) | Free | Local model presence / download progress |
| `POST` | [`/generate/docs`](#post-generatedocs-and-generateapi) | Free | AsciiDoc or MkDocs from RIDDL |
| `POST` | [`/generate/api`](#post-generatedocs-and-generateapi) | Free | Smithy, gRPC, or OpenAPI from RIDDL |
| `POST` | [`/generate/riddl`](#post-generateriddl) | Free\* | RIDDL from a description (AI) |
| `POST` | [`/generate/code`](#post-generatecode-pro) | **Pro** | Quarkus code from RIDDL |
| `POST` | [`/ai/messages`](#post-aimessages) | Free\* | One chat turn, Anthropic Messages shape |
| `POST` | [`/mcp`](#post-mcp) | Free | MCP over Streamable HTTP |
| `GET` | `/ws/echo` | Free | WebSocket echo (connectivity test only) |

\* Free on the local model; **Pro** when the effective provider is a cloud one.

Errors are always `{"error": "..."}` with an appropriate status. Unmatched
paths return `404` with an empty body.

### GET /health

Returns `200` with the plain-text body `ok`. Not JSON.

### GET /model/status

Reports whether the local model is present, and download progress if it is
being fetched. Synapify uses this to draw a progress banner.

```json
{
  "status": "model-downloading",
  "model": "qwen2.5-coder-32b-instruct-q5_k_m.gguf",
  "bytesDownloaded": 4294967296,
  "bytesTotal": 21474836480
}
```

| `status` | Meaning |
|----------|---------|
| `ready` | The model file is present and usable |
| `absent` | No model file, and none is being fetched |
| `model-downloading` | A download is in progress (or awaiting console confirmation) |
| `error` | The download failed; an extra `error` field carries the reason |

`bytesTotal` is `0` when the server could not probe the download size.

!!! note "`absent` is normal on cloud providers"
    When the active profile is a cloud one, no local model is needed and this
    endpoint reports `absent`. That is not an error condition.

### POST /generate/docs and /generate/api

Both take the same request shape:

```json
{"riddl": "domain Shop is { ??? }", "format": "mkdocs"}
```

| Field | Required | Description |
|-------|----------|-------------|
| `riddl` | yes | RIDDL source text |
| `format` | *see below* | `/generate/docs`: `asciidoc` or `mkdocs`. `/generate/api`: `smithy`, `grpc`, or `openapi` |

Response `200` returns the generated files in memory — nothing is written to
disk, and `path` is relative to your chosen output root:

```json
{"files": [{"path": "index.adoc", "content": "= Shop\n...", "format": "asciidoc"}]}
```

`400` for invalid JSON, RIDDL parse/validation errors, or an unsupported
format.

!!! warning "`format` is effectively required on `/generate/api`"
    It defaults to `asciidoc`, which `/generate/api` does not accept — omitting
    it returns `400 {"error":"unsupported format: asciidoc"}`.

### POST /generate/riddl

Generate a validated RIDDL model from a natural-language description.

```json
{
  "description": "an order-management system",
  "maxRetries": 2,
  "provider": "anthropic",
  "model": "claude-opus-4-8"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `description` | yes | The natural-language brief |
| `maxRetries` | no | Validation retry attempts (default `2`) |
| `provider` | no | A configured [profile](ai-providers.md) name; overrides the server's provider for this request only |
| `model` | no | Model id / GGUF path for the effective provider |

Response `200`:

```json
{
  "riddl": "domain Shop is { ... }",
  "valid": false,
  "errorCount": 0,
  "warningCount": 3,
  "attempts": 1,
  "messages": "..."
}
```

!!! tip "`valid` is stricter than you probably want"
    `valid` is true only when there are **no errors and no warnings**. Freshly
    generated skeletal models almost always carry advisory completeness
    warnings, so `valid: false` with `errorCount: 0` is the normal, healthy
    result. Check `errorCount` to decide whether the model is usable.

Supplying `provider`/`model` opens a transient provider for that one request
and closes it afterwards, leaving the server's resident provider untouched.
Generation is serialized, so concurrent requests queue.

| Status | When |
|--------|------|
| `202` | The local model is downloading — body is the [model status](#get-modelstatus) shape |
| `400` | Invalid JSON, unknown profile, or unusable profile configuration |
| `402` | A cloud profile was requested without Pro entitlement |
| `500` | Generation failed |
| `503` | The model download failed, or the provider is unavailable |

A per-request `provider`/`model` override skips model provisioning, so it
never returns `202`.

### POST /generate/code (Pro)

Same request and response shape as `/generate/docs`, but emits a Quarkus
project; returned files carry format `java`. The `format` field is ignored —
Quarkus is the only target. Returns `402` without a Pro subscription.

### POST /ai/messages

Answers **one** message turn in the
[Anthropic Messages](https://docs.anthropic.com/en/api/messages) shape. This
exists so a client can hold a conversation through riddlg without ever
handling API keys itself — keys and provider choice live in riddlg's
configuration, never in the request.

```json
{
  "messages": [{"role": "user", "content": "What is a bounded context?"}],
  "system": "You are a RIDDL expert.",
  "max_tokens": 1024,
  "tools": []
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `messages` | yes | Non-empty array; `content` may be a string or a block array |
| `system` | no | System prompt string |
| `max_tokens` | no | Capped at the profile's `max-tokens` |
| `tools` | no | Anthropic tool definitions — **Anthropic profiles only** |

Response `200`:

```json
{
  "role": "assistant",
  "content": [{"type": "text", "text": "A bounded context is..."}],
  "stop_reason": "end_turn",
  "model": "claude-sonnet-5"
}
```

Exactly those four fields are returned; upstream `id` and `usage` are dropped.

**Behavior depends on the active provider:**

- **Anthropic profile** — a thin passthrough. `messages`, `system`, and
  `tools` go through verbatim, `tool_use` blocks come back intact, and
  sampling parameters are stripped. This is the tool-calling path.
- **Any other provider** — plain multi-turn chat. The transcript is flattened
  into a single completion. Tool-bearing requests are refused with `501`
  rather than faking a capability the provider lacks.

The agentic loop stays on your side: tool definitions go in, `tool_use` blocks
come back, you execute them (over [`/mcp`](#post-mcp), typically) and return
`tool_result` blocks on the next turn.

| Status | When |
|--------|------|
| `202` | The local model is downloading |
| `400` | Malformed body, empty `messages`, or a non-text block on a non-Anthropic provider |
| `402` | The resident profile is a cloud one and you lack Pro |
| `501` | `tools` were supplied to a non-Anthropic provider |
| `503` | Provider unavailable / download failed |

### POST /mcp

Serves the [MCP tools](mcp-tools.md) over the Model Context Protocol's
Streamable HTTP transport. One JSON-RPC 2.0 message per request; the tools are
identical to `riddlg mcp` stdio mode.

```bash
curl -s localhost:8910/mcp -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"tools/call",
  "params":{"name":"check-completeness","arguments":{"source":"domain D is { ??? }"}}
}'
```

**Sessions.** `initialize` mints a session id and returns it in both the
`Mcp-Session-Id` and `X-Session-ID` response headers. Send either back on
subsequent requests. The id is client affinity only — the server holds no
per-session state.

**Status codes are unusual for HTTP, but correct for JSON-RPC:**

| Status | When |
|--------|------|
| `200` | Any request with an `id` — *including JSON-RPC errors*, which ride in the response body |
| `202` | A notification (no response is due) |
| `404` | `GET /mcp` — there is no SSE stream. Clients use this to detect pre-MCP riddlg versions |

Do not treat a `200` as success without checking for an `error` member in the
body.

## Client Notes

A few behaviors are worth knowing before you integrate:

1. **`Authorization: Bearer <token>` is optional and additive.** Pro-gated
   routes accept an Ossum access token, verified against the identity realm.
   The caller's tier is used for that request, so a Pro-signed-in client gets
   Pro behavior even from a server that is logged out.
2. **A bad Bearer token never returns `401`.** It is treated as absent, falling
   back to the server's own session — a forged token can never exceed what the
   server already has, and you'll simply see the usual `402`.
3. **`402` message text varies by route.** Rely on the status code and the
   `error` field, not the wording.
4. `/ws/echo` reflects frames verbatim. It is a connectivity test, not a
   generation protocol; there is no streaming endpoint.

## See Also

- [MCP Tools](mcp-tools.md) — the tool catalog behind `/mcp`
- [AI Providers](ai-providers.md) — configuring what the server generates with
- [Configuration](configuration.md) — `riddlg.server.host` / `port`
