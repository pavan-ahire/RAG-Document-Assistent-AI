
import os
from pathlib import Path

UPLOAD_DIR = "data/uploads"

def save_uploaded_files(uploaded_files):
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    saved_files = []

    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        saved_files.append(file_path)

    return saved_files
