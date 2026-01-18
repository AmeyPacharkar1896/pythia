import os
import shutil
import time
from datetime import datetime
from typing import List
from src.core.config import BACKUP_FOLDER
from src.core.logger import logger
from src.utils.file_ops import write_safe

def create_backup(file_path: str) -> None:
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

def perform_rollback(file_path: str, filename: str) -> None:
    try:
        folder = os.path.dirname(file_path)
        history_dir = os.path.join(folder, BACKUP_FOLDER)
        
        backups = [f for f in os.listdir(history_dir) if f.startswith(filename + "_") and f.endswith(".bak")]
        if not backups:
            logger.warning(f"   ⚠️ [ROLLBACK] No backups found.")
            return

        backups.sort()
        latest_backup = backups[-1]
        
        with open(os.path.join(history_dir, latest_backup), 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove the command lines that triggered the rollback
        lines = content.split('\n')
        while lines and ("UPDATE:" in lines[-1] or "ROLLBACK" in lines[-1] or not lines[-1].strip()):
            lines.pop()
        
        write_safe(file_path, "\n".join(lines))
        logger.warning(f"   ⏪ [ROLLBACK] Restored {filename} from {latest_backup}")
    except Exception as e:
        logger.error(f"   🛑 Rollback failed: {e}")