---
title: "AI Models"
description: "The default riddlg AI model, downloading alternatives, and sizing for your hardware"
---

# AI Models

riddlg's AI commands run a large language model locally through llama.cpp.
Models are ordinary [GGUF](https://huggingface.co/docs/hub/gguf) files —
you can use the tuned default or bring your own.

## The Default Model

The default model is **`qwen2.5-coder-32b-instruct-q5_k_m.gguf`**
(Qwen2.5-Coder 32B, Q5_K_M quantization, ~23 GB). It is the model riddlg's
RIDDL-generation quality is validated against, and it is sized for a 64 GB
Apple Silicon machine (see
[hardware recommendations](installation.md#hardware-requirements)).

Models live in `~/.ossum-ai/models`. Nothing is bundled with the binary —
the default model is fetched on demand.

### Downloading ahead of time

The install includes `fetch-default-model.sh` (next to the `riddlg` binary),
which downloads the default model from
[Hugging Face](https://huggingface.co/bartowski/Qwen2.5-Coder-32B-Instruct-GGUF)
into the models directory. It is idempotent — run it any time:

```bash
fetch-default-model.sh
```

The download is ~23 GB, so prefetching avoids a long wait in the middle of
your first `gen riddl`.

### Downloading on first run

Alternatively, set `OSSUM_GEN_MODEL_URL` and riddlg will download the model
automatically the first time an AI command needs it, with an optional
SHA-256 integrity check via `OSSUM_GEN_MODEL_SHA256`.

## Using Alternative Models

Any GGUF chat/instruct model works. Three ways to select one, from most to
least specific:

**1. Per command** — pass a model path directly:

```bash
riddlg gen riddl "a ticketing system" --model ~/models/qwen2.5-coder-14b-instruct-q4_k_m.gguf
```

**2. Environment variables** — change the default riddlg resolves:

| Variable | Purpose |
|----------|---------|
| `OSSUM_GEN_MODELS_DIR` | Directory holding GGUF models (default `~/.ossum-ai/models`) |
| `OSSUM_GEN_MODEL_FILE` | Default model filename to look for / download |
| `OSSUM_GEN_MODEL_URL` | URL to auto-download the default model from |
| `OSSUM_GEN_MODEL_SHA256` | Expected SHA-256 of the downloaded model (optional) |

`fetch-default-model.sh` honors the same variables, so the two mechanisms
stay in sync:

```bash
# Download and use the 14B model as your default
export OSSUM_GEN_MODEL_FILE=qwen2.5-coder-14b-instruct-q4_k_m.gguf
export OSSUM_GEN_MODEL_URL=https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF/resolve/main/qwen2.5-coder-14b-instruct-q4_k_m.gguf
fetch-default-model.sh
riddlg gen riddl "a ticketing system" -o tickets.riddl
```

**3. Configuration file** — set `riddlg.model.*` keys in
`~/.riddlg/config.conf` (HOCON). Run `riddlg config` to see the effective
settings and their documentation:

```hocon
model {
  dir = "/Users/you/.ossum-ai/models"
  default-name = "qwen2.5-coder-14b-instruct-q4_k_m.gguf"
}
```

## Choosing a Model for Your Hardware

The default 32B model gives the best RIDDL generation quality. If your
machine can't hold it, smaller quantizations of the same family are the
best fallback — expect some loss of generation fidelity as you go down.

| Model | Size | Fits comfortably on |
|-------|------|---------------------|
| [Qwen2.5-Coder-32B Q5_K_M](https://huggingface.co/bartowski/Qwen2.5-Coder-32B-Instruct-GGUF) (default) | ~23 GB | 64 GB Apple Silicon; 32 GB+ VRAM GPUs |
| [Qwen2.5-Coder-14B Q4_K_M](https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF) | ~9 GB | 24–32 GB Apple Silicon; 12–16 GB VRAM GPUs |
| [Qwen2.5-Coder-7B Q4_K_M](https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF) | ~5 GB | 16 GB Apple Silicon; 8 GB VRAM GPUs |

!!! warning "Quality varies with model size"
    riddlg validates every generated model and retries until it validates
    cleanly, so even small models produce *valid* RIDDL — but the default
    32B model is the one riddlg's generation fidelity is tuned and
    benchmarked against. Smaller models may need more retries and produce
    less complete designs.

## Generation Tuning

The generation pipeline has a few tunables (in `~/.riddlg/config.conf`
under `riddlg.generation`, shown with their defaults by `riddlg config`):

| Setting | Default | Purpose |
|---------|---------|---------|
| `n-ctx` | 16384 | llama.cpp context window |
| `max-tokens` | 6144 | Generation cap per request |
| `max-retries` | 2 | Validation retry attempts |
| `budget` | 6 | Compositional descent iterations |
| `compositional-threshold` | 240 | Auto-select compositional mode for briefs longer than this (characters) |

There is also an optional `riddlg.embed.model` setting
(`OSSUM_GEN_EMBED_MODEL`) — a small embedding GGUF used by the fidelity
benchmark's semantic checks. Most users never need it.
