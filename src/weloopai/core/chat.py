"""
Doc
"""

import logging

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain.schema import StrOutputParser
from langchain.chat_models import ChatOpenAI

from weloopai.core.store import Storer

logger = logging.getLogger("chat")


# SYSTEM_PROMPT = """Tu t'appelles Edmond. Réponds à l'utilisateur en faisant des réponses de quelques mots,
# et en utilisant des smileys (":)", ";)", etc.) pour montrer des émotions."""

WELCOME_MESSAGE = "> Bonjour, en quoi puis-je vous aider ?"

BYE_PROMPT = "Au revoir, bonne fin de journée !"

SYSTEM_PROMPT = f"""Tu es un assistant pour des tâches de questions-réponses, nommé Weloop.ai.
Utilise les documents fournis pour répondre à la question.
Si la réponse à la question n'est pas dans les documents, dis que tu n'as pas d'information sur le sujet.
Pose ensuite une ou des questions à l'utilisateur pour mieux cerner son besoin.
Important : si la réponse à la question n'est pas dans les documents, n'essaie pas de répondre à la question. Collecte seulement des informations sur le problème. Précise ensuite que tu transmettras ces informations au support technique.
Une fois que l'utilisateur n'a plus de questions, dis précisément (à la lettre près) : "{BYE_PROMPT}"
Soit respectueux et concis. Utilise trois phrases maximum par réponse, et vouvoie l'utilisateur."""

SYSTEM_PROMPT = f"""Tu es un assistant pour des tâches de questions-réponses, nommé Weloop.ai.
Tu utilises les documents fournis (appelés "ma base de connaissances") pour répondre à une question.

Si la réponse à la question est dans les documents, réponds à la question en faisant des réponses de quelques mots, et demande à l'utilisateur si cela répond bien à sa question.

Si la réponse à la question n'est pas dans les documents :
- Commence par indiquer que tu n'as pas d'information sur le sujet.
- Puis pose quelques questions à l'utilisateur pour mieux cerner son besoin.
N'essaie pas de répondre à la question, mais ne reprécise pas que tu ne peux pas y répondre. Collecte seulement des informations sur le problème. Précise ensuite que tu transmettras ces informations au support technique.

Une fois la conversation terminée, dis précisément (à la lettre près) : "{BYE_PROMPT}"
Soit respectueux et concis. Utilise trois phrases maximum par réponse, et vouvoie l'utilisateur."""

QUESTION_PROMPT = "Question: {question} \nDocuments: \n\n{documents}"

WAIT_PROMPT = "> Je cherche la réponse à votre question... "


class Chatter:

    MODEL_NAME = "gpt-3.5-turbo-0613"
    MAX_CONVERSATION_LENGTH = 100

    def __init__(self):
        self.llm = ChatOpenAI(model_name=self.MODEL_NAME, temperature=0)
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
        # Save answer
        self.messages.append(AIMessage(content=response))
        return response

    def answer_from_doc(self, question: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(QUESTION_PROMPT)
        ])
        retrieved_docs = self.retriever.get_relevant_documents(question)
        formatted_docs = "\n\n".join([f"Document {i+1}\n\n" + doc.page_content for i, doc in enumerate(retrieved_docs)])

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
        question = input()
        print(WAIT_PROMPT, end="", flush=True)
        answer = self.answer_from_doc(question)
        for _ in range(self.MAX_CONVERSATION_LENGTH):
            question = input("> ")
            answer = self.answer(question)
            if answer.strip().endswith(BYE_PROMPT):
                break
            


def start_chat() -> None:
    """
    Doc
    """
    print(WELCOME_MESSAGE)
    chatter = Chatter()
    chatter.chat()

# Utils
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
