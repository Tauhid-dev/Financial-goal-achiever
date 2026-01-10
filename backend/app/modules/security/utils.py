import os
import mimetypes
import asyncio
from datetime import datetime, timezone
from .config import SecurityConfig

def validate_upload(file_path: str, file_size: int, mime_type: str) -> None:
    """
    Raise ValueError if the upload violates any security rule:
    - Size limit
    - MIME type whitelist
    """
    if file_size > SecurityConfig.MAX_UPLOAD_SIZE:
        raise ValueError(
            f"File exceeds maximum size of {SecurityConfig.MAX_UPLOAD_SIZE} bytes"
        )
    if mime_type not in SecurityConfig.ALLOWED_MIME_TYPES:
        raise ValueError(f"Disallowed MIME type: {mime_type}")

async def schedule_auto_delete(file_path: str) -> None:
    """
    Asynchronously delete the file after AUTO_DELETE_DELAY seconds.
    Deterministic – simply sleeps then removes the file.
    """
    await asyncio.sleep(SecurityConfig.AUTO_DELETE_DELAY)
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass  # Already removed, safe to ignore
