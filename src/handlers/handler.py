import os
import time
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from src.services.memory import MemoryEngine
from src.services.brain import Brain
from src.core.config import VALID_EXTENSIONS
from src.core.logger import logger
from src.utils.file_ops import get_file_hash, write_safe
from src.utils.history import create_backup, perform_rollback

class OracleHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.memory = MemoryEngine()
        self.brain = Brain()
        self.last_hash = {}

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory: return
        time.sleep(0.5) 
        self._process_event(event.src_path, "created")

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory: return
        self._process_event(event.src_path, "modified")

    def _process_event(self, file_path: str, event_type: str) -> None:
        filename = os.path.basename(file_path)
        if filename.startswith((".", "~")) or "New Text Document" in filename: return
        
        _, ext = os.path.splitext(filename)
        if ext.lower() not in VALID_EXTENSIONS: return

        try:
            content = self._get_content(file_path)
            if not content and content != "": return
            
            # Atomic logic: Pass tasks to specialized helpers
            if "ROLLBACK" in content:
                perform_rollback(file_path, filename)
            elif "UPDATE:" in content:
                self._handle_update(file_path, filename, ext, content)
            else:
                self.memory.memorize(filename, content)
        except Exception as e:
            logger.error(f"❌ Handler Error: {e}")

    def _handle_update(self, path: str, name: str, ext: str, content: str) -> None:
        create_backup(path)
        instruction = content.strip().split('\n')[-1]
        new_code = self.brain.refactor(name, ext, content, instruction)
        write_safe(path, new_code)
        logger.info(f"✅ [SUCCESS] Refactored {name}")

    def _get_content(self, path: str) -> str:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()