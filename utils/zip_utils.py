import io
import os
import zipfile


def zip_folder_in_memory(folder_path: str) -> io.BytesIO:
    """Compress a folder into an in-memory ZIP file."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                arcname = os.path.relpath(file_path, start=folder_path)
                zip_file.write(file_path, arcname)
    buffer.seek(0)
    return buffer
