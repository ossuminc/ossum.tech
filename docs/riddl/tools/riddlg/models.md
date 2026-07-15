---
title: "AI Models"
description: "The default riddlg AI model, downloading alternatives, and sizing for your hardware"
---

# AI Models

riddlg's local AI provider runs a large language model through llama.cpp.
Models are ordinary [GGUF](https://huggingface.co/docs/hub/gguf) files — you
can use the tuned default or bring your own.

This page is about the **local model**. If you would rather generate with a
hosted service (Anthropic, Gemini, OpenAI, or anything OpenAI-compatible),
see [AI Providers](ai-providers.md) — those need no GGUF, no GPU, and no
download.

## The Default Model

The default model is **`qwen2.5-coder-32b-instruct-q5_k_m.gguf`**
(Qwen2.5-Coder 32B, Q5_K_M quantization, ~23 GB). It is the model riddlg's
RIDDL-generation quality is validated against, and it is sized for a 64 GB
Apple Silicon machine (see
[hardware recommendations](installation.md#hardware-requirements)).

Models live in `~/.ossum-ai/models`. Nothing is bundled with the binary — the
model is fetched on demand.

### Downloading on first use

riddlg ships a download URL for the default model, so **the first command that
needs the model just fetches it**. What that looks like depends on where it
happens:

| Context | Behavior |
|---------|----------|
| A terminal | You are prompted: `Download now? [y/N]`, with the model name and size |
| Headless (Synapify, daemons, CI) | The download starts automatically, logging progress |
| `riddlg serve` | AI requests answer `202` with progress until it completes — see [`/model/status`](server-api.md#get-modelstatus) |

The download is ~23 GB, so the first `gen riddl` on a fresh install will take
a while. It resumes rather than restarting if interrupted.

### Downloading ahead of time

To avoid waiting mid-task, prefetch with `fetch-default-model.sh` (installed
next to the `riddlg` binary). It is idempotent — run it any time:

```bash
fetch-default-model.sh
```

To disable automatic downloading entirely, clear the URL — riddlg will then
report a missing model instead of fetching one:

```hocon
riddlg { model { url = "" } }
```

## Using Alternative Models

Any GGUF chat/instruct model works. Three ways to select one, from most to
least specific:

**1. Per command** — pass a model path directly:

```bash
riddlg gen riddl "a ticketing system" --model ~/models/qwen2.5-coder-14b-instruct-q4_k_m.gguf
```

**2. Configuration file** — set `riddlg.model.*` keys in
`~/.riddlg/config.conf` (HOCON). Run `riddlg config` to see the effective
settings:

```hocon
riddlg {
  model {
    default-name = "qwen2.5-coder-14b-instruct-q4_k_m.gguf"
    url = "https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF/resolve/main/qwen2.5-coder-14b-instruct-q4_k_m.gguf"
  }
}
```

**3. Environment variables** — override individual keys:

| Variable | Overrides |
|----------|-----------|
| `OSSUM_GEN_MODELS_DIR` | The models directory (default `~/.ossum-ai/models`) |
| `OSSUM_GEN_MODEL_URL` | The auto-download URL |
| `OSSUM_GEN_MODEL_SHA256` | Expected SHA-256 of the download (optional integrity check) |
| `OSSUM_GEN_GPU_LAYERS` | Layers offloaded to the GPU (`99` = all, `0` = force CPU) |

!!! note "The model filename has no environment variable"
    Set `riddlg.model.default-name` in the config file to change which
    filename riddlg looks for. `OSSUM_GEN_MODEL_FILE` is read only by
    `fetch-default-model.sh`, not by riddlg itself — setting it changes what
    the script downloads without changing what riddlg loads. See
    [Configuration](configuration.md) for the full list.

```bash
# Download and use the 14B model as your default
export OSSUM_GEN_MODEL_URL=https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF/resolve/main/qwen2.5-coder-14b-instruct-q4_k_m.gguf
export OSSUM_GEN_MODEL_FILE=qwen2.5-coder-14b-instruct-q4_k_m.gguf   # for the script
fetch-default-model.sh
riddlg gen riddl "a ticketing system" -o tickets.riddl \
  --model ~/.ossum-ai/models/qwen2.5-coder-14b-instruct-q4_k_m.gguf
```

## Choosing a Model for Your Hardware

The default 32B model gives the best RIDDL generation quality. If your machine
can't hold it, smaller quantizations of the same family are the best fallback
— expect some loss of generation fidelity as you go down.

| Model | Size | Fits comfortably on |
|-------|------|---------------------|
| [Qwen2.5-Coder-32B Q5_K_M](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct-GGUF) (default) | ~23 GB | 64 GB Apple Silicon; 32 GB+ VRAM GPUs |
| [Qwen2.5-Coder-14B Q4_K_M](https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF) | ~9 GB | 24–32 GB Apple Silicon; 12–16 GB VRAM GPUs |
| [Qwen2.5-Coder-7B Q4_K_M](https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF) | ~5 GB | 16 GB Apple Silicon; 8 GB VRAM GPUs |

!!! warning "Quality varies with model size"
    riddlg validates every generated model and retries until it validates
    cleanly, so even small models produce *valid* RIDDL — but the default 32B
    model is the one riddlg's generation fidelity is tuned and benchmarked
    against. Smaller models may need more retries and produce less complete
    designs.

If none of these fit your hardware, a [cloud provider](ai-providers.md) (Pro)
sidesteps the constraint entirely — no VRAM, no download.

## Generation Tuning

The generation pipeline has a few tunables (in `~/.riddlg/config.conf` under
`riddlg.generation`, shown with their defaults by `riddlg config`):

| Setting | Default | Purpose |
|---------|---------|---------|
| `n-ctx` | 16384 | llama.cpp context window |
| `max-tokens` | 6144 | Generation cap per request (also `OSSUM_GEN_MAX_TOKENS`) |
| `max-retries` | 2 | Validation retry attempts |
| `budget` | 6 | Compositional descent iterations |
| `compositional-threshold` | 240 | Auto-select compositional mode for briefs longer than this (characters) |

`riddlg.model.gpu-layers` (default `99`, meaning all) controls GPU offload.
Setting it to `0` forces CPU inference — useful in CI, where an emulated GPU
can be slower than the CPU.

There is also an optional `riddlg.embed.model` setting
(`OSSUM_GEN_EMBED_MODEL`) — a small embedding GGUF used by the fidelity
benchmark's semantic checks. Most users never need it.

See [Configuration](configuration.md) for every setting.
