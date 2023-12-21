"""
Doc
"""

import logging

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser

from weloopai.core.chat import ChatBot
from weloopai.config.prompts import SUMMARY_PROMPT, SUMMARY_SYSTEM_PROMPT

logger = logging.getLogger("summary")


class Summarizer:
    """
    Summarize
    For now, LLM is the same as the one used for chat,
    but we might want to change that in the future
    """
    MODEL_NAME = "gpt-3.5-turbo-1106"

    def __init__(self) -> None:
        """Initialize summarizer"""
        self.llm = ChatOpenAI(model_name=self.MODEL_NAME, temperature=0)

    def summarize(self, conversation: list[BaseMessage]) -> str:
        """
        Summarize conversation
        """
        # Create prompt
        system_prompt = SystemMessage(content=SUMMARY_SYSTEM_PROMPT)
        summary_prompt = HumanMessage(content=SUMMARY_PROMPT)
        messages = [system_prompt] + conversation + [summary_prompt]
        prompt = ChatPromptTemplate.from_messages(messages)
        # Generate and display answer
        chain = prompt | self.llm | StrOutputParser()
        response = ""
        print("> ", end="", flush=True)
        for chunk in chain.stream({}):
            print(chunk, end="", flush=True)
            response += chunk
        print()
        return response
        
def summarize(conv_id: int=None) -> None:
    """
    Doc
    """
    summarizer = Summarizer()
    conversation = _load_conversation(conv_id)
    summery = summarizer.summarize(conversation)


# Utils

def _load_conversation(conv_id: int=None) -> list[BaseMessage]:
    """
    Load conversation with given id or latest conversation if not provided
    """
    conv_ids = ChatBot.list_conversations()
    if conv_id is None:
        conv_id = conv_ids[0]
        logger.info(f"No conversation id provided, using latest conversation: {conv_id}")
    if not conv_id in conv_ids:
        raise ValueError(f"Conversation id {conv_id} not found.")
    conversation = ChatBot.load_conversation(conv_id)
    return conversation
