# SORA API Management Tool

This project provides a small CLI to manage configuration and submit basic SORA API requests.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
```

## Usage

Configure your API key (or set `SORA_API_KEY` as an environment variable):

```bash
python -m sora_tool configure --api-key "sk-..."
```

Show configuration:

```bash
python -m sora_tool show-config
```

Create a video request:

```bash
python -m sora_tool create --prompt "A cinematic sunrise over the ocean" --duration 6 --size 1920x1080
```

Export a draft by identifier:

```bash
python -m sora_tool export-draft --draft-id "draft_123"
```

By default, the client uses `https://api.openai.com/v1/sora` as the base URL. Override it with
`--base-url` or `SORA_BASE_URL` if you need to point at a different endpoint.
