import os, shutil

UPLOAD_DIR = "uploads"

def save_file(student_id: int, file):
    folder = os.path.join(UPLOAD_DIR, str(student_id))
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file.filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return path

