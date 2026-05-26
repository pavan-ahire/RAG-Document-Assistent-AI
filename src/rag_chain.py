
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

CUSTOM_PROMPT = """
You are a highly accurate AI assistant.

Use ONLY the provided context to answer the question.

Rules:
- Never use outside knowledge.
- Never hallucinate information.
- If answer is not available in context, say:
  "I could not find the answer in the uploaded documents."
- Keep answers concise and grounded.
- Mention relevant details clearly.

Context:
{context}

Question:
{question}

Answer:
"""

def build_rag_chain(llm, retriever, memory):
    prompt = PromptTemplate(
        template=CUSTOM_PROMPT,
        input_variables=["context", "question"]
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
        verbose=False
    )

    return chain
