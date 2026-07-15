---
title: "AI Providers"
description: "Run riddlg's AI on the local model, or bring your own key for Anthropic, Gemini, OpenAI, or any compatible service"
---

# AI Providers

riddlg's AI features — `gen riddl`, `gen code --fill`, and the AI parts of
`serve` — run against an **AI provider**. Out of the box that provider is the
local [llama.cpp model](models.md), which is free and keeps everything on your
machine. With a [Pro subscription](index.md#free-and-pro) you can instead point
riddlg at a hosted service using **your own API key** (BYOK).

Providers are configured as named **profiles**. One profile is active at a
time, and any command can override it for a single run.

```bash
riddlg ai list                    # what's configured, and what's active
riddlg ai use anthropic --api-key-stdin
riddlg gen riddl "a pet store" -o pets.riddl    # now runs on Claude
```

!!! info "Cloud providers are a Pro feature"
    Any non-local profile requires a Pro subscription — sign in with
    `riddlg login`. The local model stays free and needs no account. Using a
    cloud provider sends your descriptions and models to that provider, which
    the local model does not.

## Provider Types

Every profile has a `type` — the wire protocol it speaks. There are five:

| Type | Use for | Default model | Default base URL | API key from |
|------|---------|---------------|------------------|--------------|
| `llama` | The local GGUF model (Free) | *the [default model](models.md)* | *in-process* | *none* |
| `anthropic` | Claude | `claude-sonnet-5` | `https://api.anthropic.com` | `ANTHROPIC_API_KEY` |
| `gemini` | Google Gemini | `gemini-3.5-flash` | `https://generativelanguage.googleapis.com` | `GEMINI_API_KEY`, then `GOOGLE_API_KEY` |
| `openai` | OpenAI Chat Completions **and every service that mimics it** | `gpt-5.6-terra` | `https://api.openai.com/v1` | `OPENAI_API_KEY` |
| `responses` | The Responses API / Open Responses spec | `gpt-5.3-codex` | `https://api.openai.com/v1` | `OPENAI_API_KEY` |

All cloud types default to a 600-second timeout. `anthropic` defaults to
16000 max tokens; `gemini`, `openai`, and `responses` default to 8192.

### openai vs responses

The `openai` type is the broadest-compatibility surface: it speaks the Chat
Completions protocol, and because the profile's `--base-url` selects the
target, one type reaches **any** service that mimics OpenAI — Ollama, vLLM,
LM Studio, llama-server, Groq, Mistral, Together, Fireworks, DeepSeek, xAI,
OpenRouter, LiteLLM, and Azure. There are no per-vendor profile types.

The `responses` type speaks the newer Responses API. Use it for OpenAI's
codex coding models (the `gpt-5-codex` family is Responses-only), or for
services that adopted Open Responses as their native surface (LM Studio,
Ollama, vLLM, OpenRouter).

riddlg absorbs the ecosystem's dialect drift so you don't have to: it picks
`max_tokens` vs `max_completion_tokens` per host and repairs itself if the
server rejects the choice, omits `temperature` for reasoning models, sends no
auth header at all to keyless local servers, and uses Azure's `api-key`
header when asked.

## Built-in Profiles

Four profiles exist without any setup — `local`, `anthropic`, `gemini`, and
`openai` — so for the common cases you only need to supply a key:

```bash
riddlg ai use anthropic --api-key-stdin     # or export ANTHROPIC_API_KEY
riddlg ai use gemini                        # GEMINI_API_KEY / GOOGLE_API_KEY
riddlg ai use openai                        # OPENAI_API_KEY
riddlg ai use local                         # back to the local model
```

There is no built-in `responses` profile — add one when you need it:

```bash
riddlg ai add codex --type responses --model gpt-5.3-codex
```

## Custom Profiles

Add as many profiles as you like. The name is yours; the `--type` tells
riddlg how to talk to it, and `--base-url` says where:

=== "Ollama"

    ```bash
    riddlg ai add ollama --type openai \
      --base-url http://localhost:11434/v1 --model qwen2.5-coder:32b
    ```

    Local servers need no key — riddlg sends no auth header when none is set.

=== "Groq"

    ```bash
    riddlg ai add groq --type openai \
      --base-url https://api.groq.com/openai/v1 \
      --model llama-3.3-70b-versatile --api-key-stdin
    ```

=== "LM Studio"

    ```bash
    riddlg ai add lmstudio --type openai \
      --base-url http://localhost:1234/v1 --model qwen2.5-coder-32b
    ```

=== "Azure OpenAI"

    ```bash
    riddlg ai add azure --type openai \
      --base-url https://YOUR-RESOURCE.openai.azure.com/openai/v1 \
      --model your-deployment --api-key-stdin
    ```

Because per-type defaults fill in whatever you omit, a minimal profile is
often enough — `riddlg ai add groq --type openai` inherits sane values for
everything else.

## Managing Profiles

### List and inspect

```bash
riddlg ai list
```

prints a table of every profile with its type, model, and where its key comes
from (`env:ANTHROPIC_API_KEY`, `config`, `keychain`, or `none`), marking the
active profile with `*`.

```bash
riddlg ai show              # effective config, keys redacted
riddlg ai show --reveal     # print keys in full
```

### Add, update, switch, remove

```bash
riddlg ai add <name> --type <type> [options]   # create (--type required)
riddlg ai set <name> [options]                 # update in place
riddlg ai use <name> [options]                 # make active (can also set up inline)
riddlg ai remove <name>                        # remove
```

`ai remove` on one of the four built-in profiles clears **your**
configuration for it; its baked-in defaults remain. You cannot remove the
active profile — switch away first.

### Test connectivity

```bash
riddlg ai test              # the active profile
riddlg ai test groq         # a specific one
```

`ai test` is a near-zero-token liveness check. For cloud profiles it pings
the service's model list (and warns if your configured model isn't in it);
for the local profile it verifies the GGUF file and GPU are present
**without** loading the model, so it costs nothing and returns immediately.

## API Keys

### Three ways to supply a key

| Method | When to use |
|--------|-------------|
| Environment variable | CI, containers, or shells that already export it |
| `--api-key-stdin` | Interactive setup — keeps the key out of shell history |
| `--api-key-keychain` | Best for workstations — the key never touches a file |
| `--api-key <value>` | Scripts only; it lands in your shell history |

```bash
# Read from stdin — nothing recorded in history
riddlg ai set anthropic --api-key-stdin

# Pipe from somewhere else
echo "$ANTHROPIC_API_KEY" | riddlg ai set anthropic --api-key-keychain
```

### Precedence

When riddlg needs a key it takes the first that resolves:

1. **The provider's environment variable** (`ANTHROPIC_API_KEY`,
   `GEMINI_API_KEY` / `GOOGLE_API_KEY`, `OPENAI_API_KEY`)
2. **The OS keychain**, when the config file holds the `@keychain` marker
3. **The config file** value
4. Otherwise the profile is keyless

An environment variable always wins, so you can override a stored key for one
shell without touching your configuration. `riddlg ai show` labels which
source each key came from.

### OS keychain storage

`--api-key-keychain` puts the secret in your platform's credential store and
writes only the literal marker `@keychain` into the config file:

| Platform | Store | Requires |
|----------|-------|----------|
| macOS | Keychain, via the `security` command | *nothing — built in* |
| Linux | Secret Service, via `secret-tool` | `libsecret-tools` / `libsecret` |

Entries are stored under service `riddlg` with the profile name as the
account, so you can inspect or revoke them with the platform's own tools.
`riddlg ai remove` clears the keychain entry too.

If a profile is marked `@keychain` but the lookup fails, riddlg reports a hard
error naming the fix rather than silently falling back to keyless — which
would surface later as a confusing `401`.

### Redaction and file permissions

Keys are never printed in full unless you ask: `riddlg ai show` and
`riddlg config` render them as `****` plus the last four characters
(just `****` for keys shorter than 8). Redaction is structural, not a regex
over the output, so no quoting or formatting surprise can leak one.

The config file is written with `0600` permissions (and `~/.riddlg` with
`0700`), re-applied on every write, and updated atomically so a crash can
never leave a half-written file containing a key. If a key-bearing config
file is readable by other users, riddlg prints an ssh-style
`UNPROTECTED API KEY FILE!` warning telling you to `chmod 600` it.

## Choosing a Provider Per Run

The active profile is the default; `--provider` overrides it for one command:

```bash
riddlg gen riddl --provider anthropic "a ticketing system" -o t.riddl
riddlg gen riddl --provider local "a ticketing system" -o t.riddl
```

`-m/--model` names a model **for the effective provider** — a GGUF path when
that resolves to the local model, or a model id for a cloud provider:

```bash
riddlg gen riddl --provider anthropic -m claude-opus-4-8 "a pet store"
```

GPU pre-flight only runs when the effective provider is the local model, so
cloud users never see a GPU error on a machine without one.

`riddlg serve` locks its provider at startup (restart to change it), but
individual requests can override it — see
[`POST /generate/riddl`](server-api.md#post-generateriddl).

## Streaming Output

`gen riddl --stream` echoes the model's output as it is produced — per token
for the local model, per chunk for cloud providers. It goes to **stderr**, so
stdout stays clean for the generated RIDDL:

```bash
riddlg gen riddl --stream "a hospital system" -o hospital.riddl
```

This is progress visibility only; the validation-and-retry loop is unchanged.

## Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| `requires an Ossum Pro subscription` | Cloud providers are Pro — run `riddlg login`, or `riddlg ai use local` |
| `has no API key` | Set one: `riddlg ai set <name> --api-key-stdin`, or export the provider's env var |
| `Unknown AI profile 'x'` | Typo — `riddlg ai list` shows the configured names |
| `does not support tool use` | Only Anthropic profiles serve tool-calling on [`/ai/messages`](server-api.md#post-aimessages) |
| Keychain lookup failed | On Linux, install `libsecret-tools`; then re-store with `--api-key-keychain` |
| No GPU error on a cloud profile | The profile didn't resolve — check `riddlg ai list` and `--provider` spelling |

## See Also

- [AI Models](models.md) — the local model, alternatives, and hardware sizing
- [Configuration](configuration.md) — the `riddlg.ai` config block in full
- [Command Reference](command-reference.md#ai) — every `ai` option
