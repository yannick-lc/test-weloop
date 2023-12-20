"""
Contains entry point for CLI
"""

import argparse
import logging

from weloopai.chat import start_chat
from weloopai.summary import summarize

logger = logging.getLogger("weloopai")


def main() -> None:
    """
    Entry point of the program.
    Parse arguments and perform actions.
    """
    parser = argparse.ArgumentParser(
        prog="weloopai",
        description="Do some stuff (CLI is a work in progress)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    debug_parser = subparsers.add_parser("chat", help="Start a chat")
    reset_parser = subparsers.add_parser("summary", help="Summarize latest conversation")
    args = parser.parse_args()

    if args.command == "chat":
        start_chat()
    elif args.command == "summary":
        summarize()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
