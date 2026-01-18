import os
import hashlib
from src.core.logger import logger

def get_file_hash(content: str) -> str:
    """Generates a hash to prevent infinite loops."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def write_safe(file_path: str, content: str) -> None:
    """Writes to file safely and logs the action."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        logger.error(f"🛑 Write Error: {e}")

def ensure_workspace(folder_path: str) -> None:
    """Self-healing: Creates the target folder if it's missing."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.warning(f"📁 Created missing workspace: '{folder_path}'")