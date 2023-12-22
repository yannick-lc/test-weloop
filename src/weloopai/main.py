"""
Contains entry point for CLI
"""

import argparse
import logging
import json
import os
from pathlib import Path

from weloopai.core.chat import start_chat
from weloopai.core.summary import summarize
from weloopai.core.store import store_as_vectors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weloopai")

logger_httpx = logging.getLogger("httpx")
logger_httpx.setLevel(logging.WARNING)
logger_chromadb = logging.getLogger("chromadb.telemetry.product.posthog")
logger_chromadb.setLevel(logging.WARNING)


def main() -> None:
    """
    Entry point of the program.
    Parse arguments and perform actions.
    """
    parser = argparse.ArgumentParser(
        prog="weloopai",
        description="Chat with our brilliant AI or summarize the latest conversation."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    chat_parser = subparsers.add_parser("chat", help="Start a chat")
    summary_parser = subparsers.add_parser("summary", help="Summarize latest conversation")
    store_parser = subparsers.add_parser("store", help="Embed documents and store as vectors")
    args = parser.parse_args()

    if args.command == "chat":
        start_chat()
    elif args.command == "summary":
        summarize()
    elif args.command == "store":
        store_as_vectors()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
