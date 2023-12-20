"""
Doc
"""

import logging

from langchain_core.documents.base import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

from weloopai.config.configuration import KNOWLEDGE_BASE_FOLDER, VECTORSTORE_FOLDER

logger = logging.getLogger("store")


class Storer:

    N_RESULTS = 2

    def __init__(self):
        self.documents = []
        self.embedding = OpenAIEmbeddings()

    def load(self) -> list[Document]:
        loader = DirectoryLoader(str(KNOWLEDGE_BASE_FOLDER), glob="**/*.txt")
        docs = loader.load()
        logger.info(f"Loaded {len(docs)} documents")
        self.documents = docs
        return self.documents

    def store(self) -> None:
        if self.documents == []:
            raise ValueError("No document loaded")
        Chroma.from_documents(
            documents=self.documents,
            embedding=self.embedding,
            persist_directory=str(VECTORSTORE_FOLDER)
        )
        logger.info(f"Embedded documents and stored as vectors in {VECTORSTORE_FOLDER}")
    
    def get_vectorstore(self) -> VectorStoreRetriever:
        vectorstore = Chroma(persist_directory=str(VECTORSTORE_FOLDER), embedding_function=self.embedding)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": self.N_RESULTS})
        return retriever

def store_as_vectors() -> None:
    """
    Doc
    """
    storer = Storer()
    storer.load()
    storer.store()
