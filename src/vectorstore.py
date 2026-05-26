import shutil
import gc
import time

from pathlib import Path

from langchain_community.vectorstores import Chroma

from src.embeddings import get_embeddings

CHROMA_DIR = "chroma_db"

# =====================================================
# CREATE VECTORSTORE
# =====================================================

def create_vectorstore(chunks):

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    vectorstore.persist()

    return vectorstore

# =====================================================
# LOAD VECTORSTORE
# =====================================================

def load_vectorstore():

    embeddings = get_embeddings()

    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

# =====================================================
# CLEAR VECTORSTORE
# =====================================================

def clear_vectorstore():

    path = Path(CHROMA_DIR)

    try:

        # Force cleanup
        gc.collect()

        # Wait briefly
        time.sleep(1)

        # Delete folder safely
        if path.exists():

            shutil.rmtree(
                path,
                ignore_errors=True
            )

        # Recreate empty folder
        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return True

    except Exception as e:

        print(f"Error clearing vectorstore: {e}")

        return False