import os
from uuid import uuid4

UPLOAD_DIR = "app/uploads"


async def save_upload_file(upload_file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    unique_filename = f"{uuid4()}_{upload_file.filename}"
    print("File :: " + unique_filename)
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    contents = await upload_file.read()
    print("Length:: " + str(len(contents)))

    print("OS path :: ")
    print(os.path.exists(file_path))

    with open(file_path, "wb") as f:
        f.write(contents)

    print("OS path :: ")
    print(os.path.exists(file_path))
    return file_path
