import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_groq import ChatGroq
from rag.rag_helper import single_index_retriever, hybrid_index_retriever
from rag.prompts import system_prompt

# Retrievers
single_retriever = RunnableLambda(single_index_retriever)
hybrid_retriever = RunnableLambda(hybrid_index_retriever)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

chatModel = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

# Building the Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# Rag pipeline:
single_rag_chain = (
    {
        "context": single_retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)),
        "input": RunnablePassthrough()
    }
    | prompt
    | chatModel
    | StrOutputParser()
)

hybrid_rag_chain = (
    {
        "context": hybrid_retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)),
        "input": RunnablePassthrough()
    }
    | prompt
    | chatModel
    | StrOutputParser()
)