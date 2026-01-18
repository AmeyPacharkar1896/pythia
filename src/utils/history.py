import os
import shutil
import time
from datetime import datetime
from typing import List
from src.core.config import BACKUP_FOLDER
from src.core.logger import logger

def create_backup(file_path: str) -> None:
    """Saves a timestamped version of the file in the hidden history folder."""
    try:
        folder = os.path.dirname(file_path)
        history_dir = os.path.join(folder, BACKUP_FOLDER)
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_name = f"{filename}_{timestamp}.bak"
        shutil.copy2(file_path, os.path.join(history_dir, backup_name))
        logger.info(f"   🛡️ [BACKUP] Saved to {BACKUP_FOLDER}/{backup_name}")
    except Exception as e:
        logger.warning(f"   ⚠️ Backup failed: {e}")

def get_backups(history_dir: str, filename: str) -> List[str]:
    """Retrieves all available backups for a specific file."""
    if not os.path.exists(history_dir): return []
    return [f for f in os.listdir(history_dir) if f.startswith(filename + "_") and f.endswith(".bak")]