"""
Configuration parameters: default folders to store documents, conversations etc
"""

from pathlib import Path


COLOR_START, COLOR_END = "\033[90m", "\033[0m" # grey color in terminal

KNOWLEDGE_BASE_FOLDER = Path("data/knowledge/documents")
VECTORSTORE_FOLDER = Path("data/knowledge/chromadb")
CONVERSATIONS_FOLDER = Path("data/conversations")
