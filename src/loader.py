
from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path

def load_documents(upload_dir):
    documents = []

    for pdf_file in Path(upload_dir).glob("*.pdf"):
        loader = PyMuPDFLoader(str(pdf_file))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = pdf_file.name

        documents.extend(docs)

    return documents
