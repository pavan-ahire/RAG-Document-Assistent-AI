
def get_retriever(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 20
        }
    )

    return retriever
