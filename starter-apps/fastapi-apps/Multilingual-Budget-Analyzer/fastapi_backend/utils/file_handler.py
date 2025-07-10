from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile


async def save_upload_file(upload_file: UploadFile, dest_dir: Path) -> Path:
    """Save an UploadFile to *dest_dir* and return the saved Path."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    original_name = upload_file.filename or "file"
    suffix = Path(original_name).suffix
    filename = f"{uuid4()}{suffix}"
    dest_path = dest_dir / filename

    # Read and write asynchronously
    file_bytes = await upload_file.read()
    dest_path.write_bytes(file_bytes)
    return dest_path 