---
title: "Installation"
description: "How to install riddlg and what hardware to run it on"
---

# Installing riddlg

`riddlg` ships as a self-contained native binary for **macOS Apple Silicon**
and **Linux x86_64**, with the llama.cpp inference libraries bundled — there
is nothing else to install.

## Hardware Requirements

The AI commands (`gen riddl`, `gen code --fill`, and the AI features of
`serve`/`mcp`) run a large language model locally and **require a GPU**.
Without one, riddlg refuses to run AI commands (pass `--allow-cpu` to
override, but CPU inference is impractically slow). Everything else —
`validate`, `gen docs`, `gen api`, plain `gen code` — runs fine on any
machine.

!!! tip "Recommended: Apple Silicon M5 Pro with 64 GB"
    For the best results, we recommend an **Apple Silicon Mac with an M5 Pro
    (or better) and 64 GB of unified memory** — for example, a Mac Mini M5
    Pro. The default AI model (~23 GB) is sized for exactly this class of
    machine and runs fully GPU-accelerated via Metal.

| Hardware | Experience |
|----------|------------|
| Apple Silicon, 64 GB unified memory (M5 Pro or better) | Recommended — default model at full speed |
| Apple Silicon, 48 GB | Works with the default model |
| Apple Silicon, 16–32 GB | Use a [smaller model](models.md#choosing-a-model-for-your-hardware) |
| Linux + NVIDIA GPU | Use the `cuda` build; ~24 GB+ VRAM for the default model, smaller models below that |
| Linux + AMD/Intel GPU | Use the `vulkan` build with a model sized to your VRAM |
| No GPU | Non-AI commands only (or `--allow-cpu` if you are very patient) |

## Homebrew

The easiest installation on macOS (Apple Silicon) and Linux (x86_64):

```bash
brew install ossuminc/tap/riddlg
```

To upgrade later:

```bash
brew upgrade riddlg
```

!!! note "Linux GPU users"
    The Homebrew Linux build is CPU-only. To use an NVIDIA, AMD, or Intel
    GPU on Linux, install the `cuda` or `vulkan` variant via
    [direct download](#direct-download) instead.

## Direct Download

Release archives are published for each version. Replace `0.3.0` with the
version you want:

=== "macOS (Apple Silicon)"

    ```bash
    curl -fLO https://storage.googleapis.com/synapify-releases/riddlg/0.3.0/riddlg-0.3.0-Darwin-arm64.tar.gz
    tar -xzf riddlg-0.3.0-Darwin-arm64.tar.gz
    export PATH="$PATH:$(pwd)/riddlg-0.3.0-Darwin-arm64/bin"
    ```

    GPU acceleration uses Metal and works out of the box.

=== "Linux (NVIDIA GPU)"

    The `cuda` variant is GPU-accelerated on NVIDIA cards (Turing/GTX 16 &
    RTX 20 series or newer). It bundles the CUDA runtime — you only need
    the NVIDIA driver installed.

    ```bash
    curl -fLO https://storage.googleapis.com/synapify-releases/riddlg/0.3.0/riddlg-0.3.0-Linux-x86_64-cuda.tar.gz
    tar -xzf riddlg-0.3.0-Linux-x86_64-cuda.tar.gz
    export PATH="$PATH:$(pwd)/riddlg-0.3.0-Linux-x86_64-cuda/bin"
    ```

=== "Linux (AMD / Intel / other GPU)"

    The `vulkan` variant runs on any GPU with a Vulkan driver (AMD, Intel,
    and NVIDIA alike).

    ```bash
    curl -fLO https://storage.googleapis.com/synapify-releases/riddlg/0.3.0/riddlg-0.3.0-Linux-x86_64-vulkan.tar.gz
    tar -xzf riddlg-0.3.0-Linux-x86_64-vulkan.tar.gz
    export PATH="$PATH:$(pwd)/riddlg-0.3.0-Linux-x86_64-vulkan/bin"
    ```

=== "Linux (CPU only)"

    For servers or machines without a GPU (non-AI commands, or CI use):

    ```bash
    curl -fLO https://storage.googleapis.com/synapify-releases/riddlg/0.3.0/riddlg-0.3.0-Linux-x86_64.tar.gz
    tar -xzf riddlg-0.3.0-Linux-x86_64.tar.gz
    export PATH="$PATH:$(pwd)/riddlg-0.3.0-Linux-x86_64/bin"
    ```

For a permanent installation, add the `export PATH=...` line to your shell
profile (`.bashrc`, `.zshrc`, etc.), or move the extracted directory
somewhere like `/opt` first.

## Linux Packages (deb / rpm)

CPU-only builds are also packaged for apt and yum/dnf. They install under
`/opt/riddlg` and put `riddlg` on your PATH via `/usr/bin/riddlg`:

=== "Debian / Ubuntu"

    ```bash
    curl -fLO https://storage.googleapis.com/synapify-releases/riddlg/0.3.0/riddlg_0.3.0_amd64.deb
    sudo dpkg -i riddlg_0.3.0_amd64.deb
    ```

=== "RHEL / Fedora"

    ```bash
    curl -fLO https://storage.googleapis.com/synapify-releases/riddlg/0.3.0/riddlg-0.3.0-1.x86_64.rpm
    sudo rpm -i riddlg-0.3.0-1.x86_64.rpm
    ```

## Verify Installation

```bash
riddlg version
```

should print the installed version (e.g. `0.3.0`), and

```bash
riddlg info
```

prints build metadata plus the compute devices llama.cpp can see. On an
Apple Silicon Mac you should see your Metal GPU listed; on Linux, your CUDA
or Vulkan device. If it warns that no GPU was detected, the AI commands
will refuse to run — check that you installed the variant matching your
hardware.

!!! note "There is no build-from-source option"
    Unlike `riddlc`, riddlg is proprietary (closed-source) software, so
    installation is via the prebuilt binaries above. The binary download is
    free; see [Free and Pro](index.md#free-and-pro).

## Next Steps

- [Command Reference](command-reference.md) - Learn the available commands
- [AI Models](models.md) - Download the default model ahead of time, or
  pick one sized for your hardware
