from __future__ import annotations

import argparse
import json
from pathlib import Path

from sora_tool.client import SoraClient
from sora_tool.config import CONFIG_FILE, Config, load_config, save_config


def _write_output(payload: dict, output: str | None) -> None:
    if output:
        Path(output).write_text(json.dumps(payload, indent=2))
        print(f"Saved response to {output}")
        return
    print(json.dumps(payload, indent=2))


def cmd_configure(args: argparse.Namespace) -> None:
    config = load_config()
    config.api_key = args.api_key or config.api_key
    config.base_url = args.base_url or config.base_url
    config.timeout_s = args.timeout or config.timeout_s
    save_config(config)
    print(f"Saved configuration to {CONFIG_FILE}")


def cmd_show(args: argparse.Namespace) -> None:
    config = load_config()
    output = {
        "api_key": config.masked_api_key(),
        "base_url": config.base_url,
        "timeout_s": config.timeout_s,
        "config_file": str(CONFIG_FILE),
    }
    print(json.dumps(output, indent=2))


def cmd_create(args: argparse.Namespace) -> None:
    config = load_config()
    client = SoraClient(config)
    response = client.create_video(args.prompt, duration_s=args.duration, size=args.size)
    payload = {"status": response.status, "response": response.payload}
    _write_output(payload, args.output)

def cmd_export(args: argparse.Namespace) -> None:
    config = load_config()
    client = SoraClient(config)
    response = client.export_draft(args.draft_id)
    payload = {"status": response.status, "response": response.payload}
    _write_output(payload, args.output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage SORA API settings and requests.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    configure = subparsers.add_parser("configure", help="Set API configuration values.")
    configure.add_argument("--api-key", help="API key to store.")
    configure.add_argument("--base-url", help="Override the SORA API base URL.")
    configure.add_argument("--timeout", type=int, help="Request timeout in seconds.")
    configure.set_defaults(func=cmd_configure)

    show = subparsers.add_parser("show-config", help="Show current configuration.")
    show.set_defaults(func=cmd_show)

    create = subparsers.add_parser("create", help="Create a video from a prompt.")
    create.add_argument("--prompt", required=True, help="Prompt to send to the SORA API.")
    create.add_argument("--duration", type=int, help="Optional duration (seconds).")
    create.add_argument("--size", help="Optional size, e.g. 1920x1080.")
    create.add_argument("--output", help="Write JSON response to a file.")
    create.set_defaults(func=cmd_create)

    export_draft = subparsers.add_parser("export-draft", help="Export a draft by identifier.")
    export_draft.add_argument("--draft-id", required=True, help="Draft identifier to export.")
    export_draft.add_argument("--output", help="Write JSON response to a file.")
    export_draft.set_defaults(func=cmd_export)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
