from langchain_groq import ChatGroq

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from flipkart.config import Config


class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.model = ChatGroq(
            model=Config.RAG_MODEL,
            temperature=0.5
        )
        self.history_store = {}

    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]

    def build_chain(self):
        retriever = self.vector_store.as_retriever()

        contextualize_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        history_aware_retriever = create_history_aware_retriever(
            self.model,
            retriever,
            contextualize_prompt
        )

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer using the provided context."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        doc_chain = create_stuff_documents_chain(
            self.model,
            qa_prompt
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            doc_chain
        )

        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )
