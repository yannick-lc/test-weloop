"""
Contains classes and functions to summarize a past conversation
"""

import logging

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser

from weloopai.core.chat import ChatBot
from weloopai.config.prompts import SUMMARY_PROMPT, SUMMARY_SYSTEM_PROMPT
from weloopai.config.configuration import COLOR_START, COLOR_END

logger = logging.getLogger("summary")


class Summarizer:
    """
    Class responsible for summurizing a saved conversation.
    """
    MODEL_NAME = "gpt-3.5-turbo-1106"

    def __init__(self) -> None:
        """
        Initialize summarizer.
        (For now, LLM is the same as the one used for chat,
        but we might want to change that in the future.)
        """
        self.llm = ChatOpenAI(model_name=self.MODEL_NAME, temperature=0)

    def summarize(self, conversation: list[BaseMessage]) -> str:
        """
        Summarize a given conversation.
        We add a new system prompt at the beginning specific to the summarization task,
        then add the conversation, and finally add a prompt at the end
        to start the summarization.
        """
        # Create prompt
        system_prompt = SystemMessage(content=SUMMARY_SYSTEM_PROMPT)
        summary_prompt = HumanMessage(content=SUMMARY_PROMPT)
        messages = [system_prompt] + conversation + [summary_prompt]
        prompt = ChatPromptTemplate.from_messages(messages)
        # Generate and display answer
        chain = prompt | self.llm | StrOutputParser()
        response = ""
        print(COLOR_START + "> ", end="", flush=True)
        for chunk in chain.stream({}):
            print(chunk, end="", flush=True)
            response += chunk
        print(COLOR_END)
        return response
    
        
def summarize(conv_id: int=None) -> None:
    """
    Instantiate a Summarizer, retrieve the conversation corresponding to the given id
    (or the latest conversation if no id is provided), and summarize it.
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
