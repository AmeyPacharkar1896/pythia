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
        print(f"!!! DEBUG: Watcher sensed CREATED event for {event.src_path}") # RAW PRINT
        if event.is_directory: return
        time.sleep(0.5) 
        self._process_event(event.src_path, "created")

    def on_modified(self, event: FileSystemEvent) -> None:
        print(f"!!! DEBUG: Watcher sensed MODIFIED event for {event.src_path}") # RAW PRINT
        if event.is_directory: return
        self._process_event(event.src_path, "modified")

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory: return
        
        # In a rename, dest_path is the new name you just typed
        new_filename = os.path.basename(event.dest_path)
        logger.info(f"🚚 [RENAMED] {os.path.basename(event.src_path)} -> {new_filename}")
        
        # Small delay to let Windows finalize the file lock
        time.sleep(0.5) 
        self._process_event(event.dest_path, "created")

    def _process_event(self, file_path: str, event_type: str) -> None:
        filename = os.path.basename(file_path)
        
        if filename.startswith((".", "~")) or "New Text Document" in filename:
            return
        
        _, ext = os.path.splitext(filename)
        if ext.lower() not in VALID_EXTENSIONS:
            return

        try:
            if not os.path.exists(file_path): return
            
            size = os.path.getsize(file_path)
            content = self._get_content(file_path)

            # 🔮 CASE 1: Brand New Empty File -> GENERATE
            if size == 0 and event_type == "created":
                logger.info(f"🔮 [PROMPT] '{filename}' detected. Fulfilling prophecy...")
                self._handle_generation(file_path, filename, ext)
            
            # 📝 CASE 2: File has content -> UPDATE, ROLLBACK, or MEMORIZE
            elif size > 0:
                # Prevent infinite loops if the Oracle just wrote this
                current_hash = get_file_hash(content)
                if self.last_hash.get(filename) == current_hash:
                    return

                if "ROLLBACK" in content:
                    perform_rollback(file_path, filename)
                elif "UPDATE:" in content:
                    self._handle_update(file_path, filename, ext, content)
                else:
                    logger.info(f"🧠 [LEARNING] Absorbed '{filename}'")
                    self.memory.memorize(filename, content)
                    self.last_hash[filename] = current_hash

        except Exception as e:
            logger.error(f"❌ Handler Error for {filename}: {e}")

    def _handle_generation(self, path: str, name: str, ext: str) -> None:
        # Placeholder text so the user knows it's working
        write_safe(path, "🔮 The Oracle is searching its memories...")
        
        # Search RAG Memory
        query = name.replace("_", " ")
        results = self.memory.recall(query)
        
        context_str = ""
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                context_str += f"\n--- MEMORY: {results['metadatas'][0][i]['filename']} ---\n{doc}\n"

        # Call AI
        new_content = self.brain.generate(name, ext, context_str)
        
        # Write and update hash to prevent loop
        self.last_hash[name] = get_file_hash(new_content)
        write_safe(path, new_content)
        logger.info(f"✅ [SUCCESS] Generated {name}")

    def _handle_update(self, path: str, name: str, ext: str, content: str) -> None:
        create_backup(path)
        instruction = content.strip().split('\n')[-1]
        new_code = self.brain.refactor(name, ext, content, instruction)
        
        self.last_hash[name] = get_file_hash(new_code)
        write_safe(path, new_code)
        logger.info(f"✅ [SUCCESS] Refactored {name}")

    def _get_content(self, path: str) -> str:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()