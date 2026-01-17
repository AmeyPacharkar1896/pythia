import os
import time
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from src.memory import MemoryEngine
from src.brain import Brain
from src.config import VALID_EXTENSIONS, BACKUP_FOLDER
from src.logger import logger 

class OracleHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.memory: MemoryEngine = MemoryEngine()
        self.brain: Brain = Brain()
        self.last_hash: Dict[str, str] = {} 

    def _get_file_hash(self, content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory: return
        time.sleep(0.5) 
        self._handle_event(event.src_path, event_type="created")

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory: return
        self._handle_event(event.src_path, event_type="modified")

    def on_deleted(self, event: FileSystemEvent) -> None:
        if event.is_directory: return
        filename: str = os.path.basename(event.src_path)
        if filename in self.last_hash: del self.last_hash[filename]
        
        _, ext = os.path.splitext(filename)
        if ext.lower() in VALID_EXTENSIONS:
            logger.warning(f"❌ [DELETED] '{filename}' - Forgot from memory.")
            self.memory.forget(filename)

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory: return
        old_filename: str = os.path.basename(event.src_path)
        self.memory.forget(old_filename)
        self._handle_event(event.dest_path, event_type="created")

    def _handle_event(self, file_path: str, event_type: str) -> None:
        filename: str = os.path.basename(file_path)
        if filename.startswith(".") or filename.startswith("~"): return
        if "New Text Document" in filename: return 
        
        _, ext = os.path.splitext(filename)
        if ext.lower() not in VALID_EXTENSIONS: return

        try:
            if not os.path.exists(file_path): return
            size: int = os.path.getsize(file_path)
        except OSError:
            return

        # 1. NEW FILE
        if size == 0 and event_type == "created":
            if ext == ".mermaid":
                self._handle_visualization(file_path, filename)
            else:
                logger.info(f"🔮 [PROMPT] '{filename}' detected.")
                self._fulfill_prophecy(file_path, filename, ext)
        
        # 2. EXISTING FILE
        elif size > 0:
            if ext == ".mermaid": return
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content: str = f.read()

                current_hash: str = self._get_file_hash(content)
                if self.last_hash.get(filename) == current_hash:
                    return

                if "The Oracle is" in content[:100]: return

                lines: List[str] = content.strip().split('\n')
                last_line: str = lines[-1].strip() if lines else ""

                if "ROLLBACK" in last_line:
                    logger.warning(f"✨ [COMMAND] Rollback requested in '{filename}'")
                    self._perform_rollback(file_path, filename)
                
                elif "UPDATE:" in last_line:
                    logger.info(f"✨ [EDIT REQUEST] Detected command in '{filename}'")
                    logger.info(f"   📝 Instruction: {last_line}")
                    self._perform_edit(file_path, filename, ext, content, last_line)
                
                else:
                    logger.info(f"🧠 [LEARNING] Absorbed '{filename}' into memory.")
                    self._memorize(file_path, filename)
            
            except Exception as e:
                logger.error(f"Error processing file: {e}")

    def _handle_visualization(self, file_path: str, filename: str) -> None:
        folder: str = os.path.dirname(file_path)
        base_name: str = os.path.splitext(filename)[0]
        source_file: Optional[str] = None
        code_exts: List[str] = [e for e in VALID_EXTENSIONS if e not in ['.txt', '.md', '.mermaid']]
        
        for possible_ext in code_exts:
            possible_path = os.path.join(folder, base_name + possible_ext)
            if os.path.exists(possible_path):
                source_file = possible_path
                break
        
        if source_file:
            logger.info(f"🎨 [VISUALIZE] generating diagram for '{os.path.basename(source_file)}'")
            self._generate_diagram(file_path, source_file)
        else:
            logger.error(f"⚠️ [ERROR] Could not find source code for '{filename}'.")

    def _perform_edit(self, file_path: str, filename: str, ext: str, content: str, instruction: str) -> None:
        self._create_backup(file_path)
        new_content: str = self.brain.refactor(filename, ext, content, instruction)
        self._write_safe(file_path, filename, new_content)
        logger.info(f"✅ [SUCCESS] Refactored {filename}")

    def _fulfill_prophecy(self, file_path: str, filename: str, ext: str) -> None:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("🔮 The Oracle is searching its memories...")
            
            query: str = filename.replace("_", " ")
            logger.info(f"   🔍 Searching memory for: '{query}'...")
            results = self.memory.recall(query)
            context_str: str = ""
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    context_str += f"\n--- MEMORY FROM {results['metadatas'][0][i]['filename']} ---\n{doc}\n"
                logger.info(f"   💡 Context found.")
            else:
                logger.info("   🌑 No context found. Pure generation.")

            content: str = self.brain.generate(filename, ext, context_str)
            self._write_safe(file_path, filename, content)
            logger.info(f"✅ [SUCCESS] Written to {filename}")
        except Exception as e:
            logger.error(f"🛑 Generation Error: {e}")

    def _generate_diagram(self, diagram_path: str, source_path: str) -> None:
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                code_content: str = f.read()
            diagram_code: str = self.brain.visualize(os.path.basename(source_path), code_content)
            with open(diagram_path, 'w', encoding='utf-8') as f:
                f.write(diagram_code)
            logger.info(f"✅ [SUCCESS] Diagram generated.")
        except Exception as e:
            logger.error(f"🛑 Error: {e}")

    def _create_backup(self, file_path: str) -> None:
        try:
            folder: str = os.path.dirname(file_path)
            history_dir: str = os.path.join(folder, BACKUP_FOLDER)
            
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
                try:
                    import ctypes
                    ctypes.windll.kernel32.SetFileAttributesW(history_dir, 2)
                except: pass

            timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name: str = os.path.basename(file_path)
            backup_name: str = f"{original_name}_{timestamp}.bak"
            shutil.copy2(file_path, os.path.join(history_dir, backup_name))
            logger.info(f"   🛡️ [BACKUP] Saved to {BACKUP_FOLDER}/{backup_name}")
        except Exception as e:
            logger.warning(f"   ⚠️ Backup failed: {e}")

    def _perform_rollback(self, file_path: str, filename: str) -> None:
        try:
            folder: str = os.path.dirname(file_path)
            history_dir: str = os.path.join(folder, BACKUP_FOLDER)
            
            if not os.path.exists(history_dir):
                logger.warning(f"   ⚠️ [ROLLBACK] No history folder.")
                return

            backups: List[str] = [f for f in os.listdir(history_dir) if f.startswith(filename + "_") and f.endswith(".bak")]
            if not backups:
                logger.warning(f"   ⚠️ [ROLLBACK] No backups found.")
                return

            backups.sort()
            latest_backup: str = backups[-1]
            
            with open(os.path.join(history_dir, latest_backup), 'r', encoding='utf-8', errors='ignore') as f:
                content: str = f.read()

            lines: List[str] = content.split('\n')
            while lines:
                last_line: str = lines[-1].strip()
                if not last_line or "UPDATE:" in last_line or "ROLLBACK" in last_line:
                    lines.pop() 
                else:
                    break 
            
            cleaned_content: str = "\n".join(lines)
            
            logger.info(f"   ⏳ Waiting for editor to release file...")
            time.sleep(0.5)

            self._write_safe(file_path, filename, cleaned_content)
            logger.warning(f"   ⏪ [ROLLBACK] Restored {filename} from {latest_backup}")

        except Exception as e:
            logger.error(f"   🛑 Rollback failed: {e}")

    def _write_safe(self, file_path: str, filename: str, content: str) -> None:
        content_hash: str = self._get_file_hash(content)
        self.last_hash[filename] = content_hash
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def _memorize(self, file_path: str, filename: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text: str = f.read()
            self.memory.memorize(filename, text)
        except: pass