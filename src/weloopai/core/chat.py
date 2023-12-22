"""
Contains classes and functions to manage a conversation with a user
"""

import logging
import pickle
import time

from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import StrOutputParser
from langchain.chat_models import ChatOpenAI

from weloopai.core.store import KnowledgeStore
from weloopai.config.prompts import CHAT_SYSTEM_PROMPT, QUESTION_PROMPT_TEMPLATE, WELCOME_MESSAGE, BYE_MESSAGE
from weloopai.config.configuration import CONVERSATIONS_FOLDER, COLOR_START, COLOR_END

logger = logging.getLogger("chat")


class ChatBot:
    """
    Class responsible for managing a conversation with a user
    (storing messages, generating answers, etc.)
    """
    MODEL_NAME = "gpt-3.5-turbo-1106"
    MAX_CONVERSATION_LENGTH = 100

    def __init__(self, conv_id=None):
        """Initialize the conversation"""
        # Generate an id for the conversation
        if conv_id is None:
            conv_id = int(time.time()*1000) # generate a unique id
        self.conv_id = conv_id
        logger.info(f"Started conversation with id {self.conv_id}")

        # Define the language model and the knowledge base
        self.llm = ChatOpenAI(
            model_name=self.MODEL_NAME,
            temperature=0,
            model_kwargs={"frequency_penalty": 1.0}
        )
        self.vectorstore = KnowledgeStore().get_vectorstore()

        # Initialize the conversation with the system prompt
        self.messages = [
            SystemMessage(content=CHAT_SYSTEM_PROMPT)
        ]

    def answer(self, question: str) -> str:
        """
        Generate an answer to a question, and add both the question
        and the answer to the conversation to remember them later
        """
        # Create prompt
        self.messages.append(HumanMessage(content=question))
        prompt = ChatPromptTemplate.from_messages(self.messages)
        chain = prompt | self.llm | StrOutputParser()

        # Generate and display answer
        response = ""
        print(COLOR_START + "> ", end="", flush=True)
        for chunk in chain.stream({}):
            print(chunk, end="", flush=True)
            response += chunk
        print(COLOR_END) # end gray color

        # Save and return answer
        self.messages.append(AIMessage(content=response))
        return response

    def answer_from_doc(self, question: str) -> str:
        """
        Generate an answer to a question using the documents
        from the knowledge base, and add both the question
        Add the question and answer to the conversation
        """

        # Generate the prompt to retrieve documents
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=CHAT_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(QUESTION_PROMPT_TEMPLATE)
        ])

        # Retrieve documents
        retrieved_docs = self.vectorstore.get_relevant_documents(question)
        formatted_docs = "\n\n".join([
            (f"Document {i+1}\n\n" + doc.page_content)
            for i, doc in enumerate(retrieved_docs)
        ])

        # Prepare prompt that uses retrieved documents to generate answer
        parameters = {"question": question, "documents": formatted_docs}
        self.messages = prompt.invoke(parameters).messages
        rag_chain = (
            prompt
            | self.llm
            | StrOutputParser()
        )

        # Generate and display answer
        response = ""
        print(COLOR_START + "> ", end="", flush=True)
        for chunk in rag_chain.stream(parameters):
            print(chunk, end="", flush=True)
            response += chunk
        print(COLOR_END) # end gray color

        # Save and return answer
        self.messages.append(AIMessage(content=response))
        return response

    def chat(self):
        """
        Start a conversation with the user: ask for a question,
        look for an answer in the docs, generate the answer,
        and follow up with more questions/answers if necessary.
        """
        # Start by asking for a question and look for an answer in the docs
        print(COLOR_START + "> " + WELCOME_MESSAGE + COLOR_END)
        question = input("> ")
        answer = self.answer_from_doc(question)
        self.save_conversation()

        # Follow up with more questions/answers
        for _ in range(self.MAX_CONVERSATION_LENGTH):
            question = input("> ")
            answer = self.answer(question)
            self.save_conversation()

            conversation_is_over = answer.strip().endswith(BYE_MESSAGE)
            if conversation_is_over:
                break

    # Utils to save and load conversations
            
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

    def save_conversation(self) -> None:
        """Save current conversation in pickle file"""
        messages = self.messages[1:] # remove system prompt
        with open(CONVERSATIONS_FOLDER / f"{self.conv_id}.pkl", "wb") as f:
            pickle.dump(messages, f)


def start_chat() -> None:
    """Instantiate a ChatBot and start a conversation"""
    chatbot = ChatBot()
    chatbot.chat()
