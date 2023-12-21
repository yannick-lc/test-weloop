"""
Doc
"""

import logging
import pickle
import time

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage
from langchain.schema import StrOutputParser
from langchain.chat_models import ChatOpenAI

from weloopai.core.store import Storer
from weloopai.config.prompts import SYSTEM_PROMPT, QUESTION_PROMPT, WELCOME_MESSAGE, WAIT_PROMPT, BYE_PROMPT
from weloopai.config.configuration import CONVERSATIONS_FOLDER

logger = logging.getLogger("chat")


class ChatBot:

    MODEL_NAME = "gpt-3.5-turbo-1106"
    MAX_CONVERSATION_LENGTH = 100

    def __init__(self, conv_id=None):
        if conv_id is None:
            conv_id = int(time.time()*1000) # generate a unique id
        self.conv_id = conv_id
        logger.info(f"Started conversation with id {self.conv_id}")

        self.llm = ChatOpenAI(
            model_name=self.MODEL_NAME,
            temperature=0,
            model_kwargs={"frequency_penalty": 1.0}
        )
        self.messages = [
            SystemMessage(content=SYSTEM_PROMPT)
        ]
        self.retriever = Storer().get_vectorstore()

    def answer(self, question: str) -> str:
        # Create prompt
        self.messages.append(HumanMessage(content=question))
        prompt = ChatPromptTemplate.from_messages(self.messages)
        chain = prompt | self.llm | StrOutputParser()
        # Generate and display answer
        response = ""
        print("> ", end="", flush=True)
        for chunk in chain.stream({}):
            print(chunk, end="", flush=True)
            response += chunk
        print()
        self.messages.append(AIMessage(content=response))
        return response

    def answer_from_doc(self, question: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(QUESTION_PROMPT)
        ])
        retrieved_docs = self.retriever.get_relevant_documents(question)
        formatted_docs = "\n\n".join([
            (f"Document {i+1}\n\n" + doc.page_content)
            for i, doc in enumerate(retrieved_docs)
        ])

        parameters = {"question": question, "documents": formatted_docs}
        self.messages = prompt.invoke(parameters).messages
        rag_chain = (
            prompt
            | self.llm
            | StrOutputParser()
        )
        response = ""
        for chunk in rag_chain.stream(parameters):
            print(chunk, end="", flush=True)
            response += chunk
        print()
        self.messages.append(AIMessage(content=response))
        return response

    def chat(self):
        print(WELCOME_MESSAGE)
        question = input("> ")
        print(WAIT_PROMPT, end="", flush=True)
        answer = self.answer_from_doc(question)
        for _ in range(self.MAX_CONVERSATION_LENGTH):
            question = input("> ")
            answer = self.answer(question)
            self._save_conversation()
            # Stop if conversation is over
            if answer.strip().endswith(BYE_PROMPT):
                break

    # Save and load utils
            
    @classmethod
    def list_conversations(cls) -> list[int]:
        """Return a list of saved conversation ids"""
        # list files by reverse chrionological order
        files = sorted(CONVERSATIONS_FOLDER.glob('*.pkl'), reverse=True)
        ids = [int(file.name.split('.')[0]) for file in files]
        return ids
            
    @classmethod
    def load_conversation(cls, conv_id: int) -> list[BaseMessage]:
        """Load and return a conversation from pickle file"""
        with open(CONVERSATIONS_FOLDER / f"{conv_id}.pkl", "rb") as f:
            messages = pickle.load(f)
        return messages

    def _save_conversation(self) -> None:
        """Save current conversation in pickle file"""
        messages = self.messages[1:] # remove system prompt
        with open(CONVERSATIONS_FOLDER / f"{self.conv_id}.pkl", "wb") as f:
            pickle.dump(messages, f)




def start_chat() -> None:
    """
    Doc
    """
    chatter = ChatBot()
    chatter.chat()
