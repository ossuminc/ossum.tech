---
title: "Configuration"
description: "The riddlg config file, every setting and its default, and environment variables"
---

# Configuration

`riddlg` reads its settings from a [HOCON](https://github.com/lightbend/config)
config file, the same way `riddlc` does. Everything has a working default, so
a config file is optional — you only set what you want to change.

To see the settings riddlg is actually using, fully resolved:

```bash
riddlg config
```

API keys are redacted in that output.

## Where Settings Come From

Settings resolve in this order, **highest precedence first**:

1. **CLI flags** — override everything, at the call site
2. **`OSSUM_GEN_*` environment variables** — one setting each
3. **Config files** — see below
4. **Baked-in defaults**

Config files are themselves layered, again highest first:

| Order | Location | Purpose |
|-------|----------|---------|
| 1 | `$RIDDLG_CONFIG` | The file named by this environment variable, if set |
| 2 | `./riddlg.conf` | Per-project, in the current working directory |
| 3 | `~/.riddlg/config.conf` | Your personal default |

Files merge with fallback, so a file only needs the keys it changes;
everything else falls through to the next file and then to the defaults.

!!! note "Where `riddlg ai` writes"
    The `riddlg ai` commands write to `$RIDDLG_CONFIG` if set, otherwise to
    `~/.riddlg/config.conf` — never to `./riddlg.conf`. They rewrite only
    the keys you have actually set, so baked-in defaults are never frozen
    into your file and upgrading riddlg still upgrades the settings you never
    touched. Comments are **not** preserved across a rewrite.

## Settings Reference

The complete set of settings with their defaults:

```hocon
riddlg {
  model {
    # Directory holding GGUF models (download-on-first-run lands here).
    dir = "~/.ossum-ai/models"
    # Default model filename when --model is not given.
    default-name = "qwen2.5-coder-32b-instruct-q5_k_m.gguf"
    # URL to auto-download the default model from (first AI use).
    # Clear it to disable auto-download entirely.
    url = "https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct-GGUF/resolve/main/qwen2.5-coder-32b-instruct-q5_k_m.gguf"
    # Optional expected sha256 of the downloaded model.
    sha256 = ""
    # Layers offloaded to the GPU (99 = all). 0 forces CPU.
    gpu-layers = 99
  }
  # Optional small embedding GGUF for the fidelity benchmark's semantic term.
  embed { model = "" }
  server {
    host = "127.0.0.1"
    port = 8910
  }
  generation {
    max-retries = 2               # validation retry attempts
    budget = 6                    # compositional descent iterations
    n-ctx = 16384                 # llama.cpp context window
    max-tokens = 6144             # generation cap per request
    compositional-threshold = 240 # auto-select compositional above this brief length
  }
  # Run model-loading commands on CPU even without a GPU (very slow).
  allow-cpu = false
  ai {
    # Active provider profile (env RIDDLG_AI_PROVIDER overrides).
    provider = "local"
    # Named provider profiles; add more with `riddlg ai add`.
    profiles {
      local {
        type = llama   # uses the riddlg.model.* keys above
      }
      anthropic {
        type = anthropic
        api-key = ""
        model = "claude-sonnet-5"
        base-url = "https://api.anthropic.com"
        max-tokens = 16000
        timeout-seconds = 600
      }
      gemini {
        type = gemini
        api-key = ""
        model = "gemini-3.5-flash"
        base-url = "https://generativelanguage.googleapis.com"
        max-tokens = 8192
        timeout-seconds = 600
      }
      openai {
        type = openai
        api-key = ""
        model = "gpt-5.6-terra"
        base-url = "https://api.openai.com/v1"
        max-tokens = 8192
        token-param = "auto"
        timeout-seconds = 600
      }
    }
  }
}
```

!!! tip "`riddlg config` output has no `riddlg { }` wrapper"
    It prints the tree rooted *inside* `riddlg`, so what you see starts at
    `model { ... }`. Your config file still needs the `riddlg { }` wrapper
    (or dotted keys like `riddlg.server.port = 9000`).

### AI profile keys

Profiles under `riddlg.ai.profiles` are normally managed with
[`riddlg ai`](ai-providers.md) rather than by hand. Each accepts:

| Key | Purpose |
|-----|---------|
| `type` | `llama`, `anthropic`, `gemini`, `openai`, or `responses` |
| `api-key` | The key, or the literal `@keychain` marker |
| `model` | Model id (cloud) or GGUF path (local) |
| `base-url` | Endpoint base URL |
| `max-tokens` | Generation cap per request |
| `timeout-seconds` | Request timeout (default 600) |
| `token-param` | `auto` (default), `max_tokens`, or `max_completion_tokens` |
| `auth` | `bearer` (default) or `api-key-header` (Azure) |

Missing keys fall back to sensible per-type defaults, so
`groq { type = openai }` is a valid profile. See
[AI Providers](ai-providers.md#provider-types) for the per-type defaults.

## Environment Variables

Each variable overrides one config key (env beats file, file beats default):

| Variable | Overrides | Notes |
|----------|-----------|-------|
| `RIDDLG_CONFIG` | *the config file path* | Read from **and** written to by `riddlg ai` |
| `RIDDLG_AI_PROVIDER` | `riddlg.ai.provider` | The active profile name |
| `OSSUM_GEN_MODELS_DIR` | `riddlg.model.dir` | |
| `OSSUM_GEN_MODEL_URL` | `riddlg.model.url` | |
| `OSSUM_GEN_MODEL_SHA256` | `riddlg.model.sha256` | |
| `OSSUM_GEN_GPU_LAYERS` | `riddlg.model.gpu-layers` | `0` forces CPU inference |
| `OSSUM_GEN_EMBED_MODEL` | `riddlg.embed.model` | |
| `OSSUM_GEN_HOST` | `riddlg.server.host` | |
| `OSSUM_GEN_PORT` | `riddlg.server.port` | |
| `OSSUM_GEN_MAX_TOKENS` | `riddlg.generation.max-tokens` | |
| `OSSUM_GEN_ALLOW_CPU` | `riddlg.allow-cpu` | **Exactly `1`** means true |

API keys have their own variables — see
[AI Providers](ai-providers.md#precedence). They are not `OSSUM_GEN_*`
overrides; they take precedence over the config file entirely:
`ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`.

!!! note "Values that must be numbers"
    `OSSUM_GEN_PORT`, `OSSUM_GEN_GPU_LAYERS`, and `OSSUM_GEN_MAX_TOKENS` are
    parsed as integers. A non-numeric value is ignored silently and the config
    value is used instead.

## Examples

Serve on a different port for a project, via `./riddlg.conf`:

```hocon
riddlg {
  server { port = 9000 }
}
```

Use a smaller local model:

```hocon
riddlg {
  model {
    default-name = "qwen2.5-coder-14b-instruct-q4_k_m.gguf"
    url = "https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF/resolve/main/qwen2.5-coder-14b-instruct-q4_k_m.gguf"
  }
}
```

Run the local model on CPU in CI, with a short generation cap:

```bash
export OSSUM_GEN_GPU_LAYERS=0
export OSSUM_GEN_MAX_TOKENS=128
export OSSUM_GEN_ALLOW_CPU=1
```

## See Also

- [AI Providers](ai-providers.md) — managing profiles and keys
- [AI Models](models.md) — model selection and tuning
- [Server API](server-api.md) — what `riddlg serve` exposes
