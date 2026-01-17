import os
import time
import shutil
import hashlib
from datetime import datetime
from watchdog.events import FileSystemEventHandler
from src.memory import MemoryEngine
from src.brain import Brain

class OracleHandler(FileSystemEventHandler):
    def __init__(self):
        self.memory = MemoryEngine()
        self.brain = Brain()
        self.last_hash = {} 

    def _get_file_hash(self, content):
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def on_created(self, event):
        if event.is_directory: return
        time.sleep(0.5) 
        self._handle_event(event.src_path, event_type="created")

    def on_modified(self, event):
        if event.is_directory: return
        self._handle_event(event.src_path, event_type="modified")

    def on_deleted(self, event):
        if event.is_directory: return
        filename = os.path.basename(event.src_path)
        if filename in self.last_hash: del self.last_hash[filename]
        
        valid_exts = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.sql']
        _, ext = os.path.splitext(filename)
        if ext.lower() in valid_exts:
            print(f"\n❌ [DELETED] '{filename}'")
            self.memory.forget(filename)

    def on_moved(self, event):
        if event.is_directory: return
        old_filename = os.path.basename(event.src_path)
        self.memory.forget(old_filename)
        self._handle_event(event.dest_path, event_type="created")

    def _handle_event(self, file_path, event_type):
        filename = os.path.basename(file_path)
        if filename.startswith(".") or filename.startswith("~"): return
        if "New Text Document" in filename: return 
        
        valid_exts = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.sql', '.mermaid']
        _, ext = os.path.splitext(filename)
        if ext.lower() not in valid_exts: return

        try:
            if not os.path.exists(file_path): return
            size = os.path.getsize(file_path)
        except OSError:
            return

        # 1. NEW FILE
        if size == 0 and event_type == "created":
            if ext == ".mermaid":
                self._handle_visualization(file_path, filename)
            else:
                print(f"\n🔮 [PROMPT] '{filename}'")
                self._fulfill_prophecy(file_path, filename, ext)
        
        # 2. EXISTING FILE
        elif size > 0:
            if ext == ".mermaid": return
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Anti-Loop Check
                current_hash = self._get_file_hash(content)
                if self.last_hash.get(filename) == current_hash:
                    return

                if "The Oracle is" in content[:100]: return

                lines = content.strip().split('\n')
                last_line = lines[-1].strip() if lines else ""

                if "ROLLBACK" in last_line:
                    print(f"\n✨ [COMMAND] Rollback requested in '{filename}'")
                    self._perform_rollback(file_path, filename)
                
                elif "UPDATE:" in last_line:
                    print(f"\n✨ [EDIT REQUEST] Detected command in '{filename}'")
                    print(f"   📝 Instruction: {last_line}")
                    self._perform_edit(file_path, filename, ext, content, last_line)
                
                else:
                    print(f"\n🧠 [LEARNING] '{filename}'")
                    self._memorize(file_path, filename)
            
            except Exception as e:
                print(f"Error processing file: {e}")

    def _handle_visualization(self, file_path, filename):
        folder = os.path.dirname(file_path)
        base_name = os.path.splitext(filename)[0]
        source_file = None
        for possible_ext in ['.py', '.js', '.html', '.css', '.sql', '.json']:
            possible_path = os.path.join(folder, base_name + possible_ext)
            if os.path.exists(possible_path):
                source_file = possible_path
                break
        
        if source_file:
            print(f"\n🎨 [VISUALIZE] Generating diagram for '{os.path.basename(source_file)}'")
            self._generate_diagram(file_path, source_file)
        else:
            print(f"\n⚠️ [ERROR] Could not find source code for '{filename}'.")

    def _perform_edit(self, file_path, filename, ext, content, instruction):
        self._create_backup(file_path)
        new_content = self.brain.refactor(filename, ext, content, instruction)
        self._write_safe(file_path, filename, new_content)
        print(f"✅ [SUCCESS] Refactored {filename}")

    def _fulfill_prophecy(self, file_path, filename, ext):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("🔮 The Oracle is searching its memories...")
            
            query = filename.replace("_", " ")
            print(f"   🔍 Searching memory for: '{query}'...")
            results = self.memory.recall(query)
            context_str = ""
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    context_str += f"\n--- MEMORY FROM {results['metadatas'][0][i]['filename']} ---\n{doc}\n"
                print(f"   💡 Context found.")
            else:
                print("   🌑 No context found. Pure generation.")

            content = self.brain.generate(filename, ext, context_str)
            self._write_safe(file_path, filename, content)
            print(f"✅ [SUCCESS] Written to {filename}")
        except Exception as e:
            print(f"🛑 Generation Error: {e}")

    def _generate_diagram(self, diagram_path, source_path):
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            diagram_code = self.brain.visualize(os.path.basename(source_path), code_content)
            with open(diagram_path, 'w', encoding='utf-8') as f:
                f.write(diagram_code)
            print(f"✅ [SUCCESS] Diagram generated.")
        except Exception as e:
            print(f"🛑 Error: {e}")

    def _create_backup(self, file_path):
        try:
            folder = os.path.dirname(file_path)
            history_dir = os.path.join(folder, ".pythia_history")
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
                try:
                    import ctypes
                    ctypes.windll.kernel32.SetFileAttributesW(history_dir, 2)
                except: pass

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = os.path.basename(file_path)
            backup_name = f"{original_name}_{timestamp}.bak"
            shutil.copy2(file_path, os.path.join(history_dir, backup_name))
            print(f"   🛡️ [BACKUP] Saved to .pythia_history/{backup_name}")
        except Exception as e:
            print(f"   ⚠️ Backup failed: {e}")

    def _perform_rollback(self, file_path, filename):
        try:
            folder = os.path.dirname(file_path)
            history_dir = os.path.join(folder, ".pythia_history")
            
            if not os.path.exists(history_dir):
                print(f"   ⚠️ [ROLLBACK] No history folder.")
                return

            backups = [f for f in os.listdir(history_dir) if f.startswith(filename + "_") and f.endswith(".bak")]
            if not backups:
                print(f"   ⚠️ [ROLLBACK] No backups found.")
                return

            backups.sort()
            latest_backup = backups[-1]
            
            # Read backup content
            with open(os.path.join(history_dir, latest_backup), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # DEBUG: Prove what we found
            print(f"   🔎 [DEBUG] Reading backup: {latest_backup}")
            print(f"   🔎 [DEBUG] Backup size: {len(content)} bytes")

            # Clean content
            lines = content.split('\n')
            while lines:
                last_line = lines[-1].strip()
                if not last_line or "UPDATE:" in last_line or "ROLLBACK" in last_line:
                    lines.pop() 
                else:
                    break 
            
            cleaned_content = "\n".join(lines)
            
            # 🛑 CRITICAL FIX: WAIT FOR VS CODE TO RELEASE FILE HANDLE
            print(f"   ⏳ Waiting for editor to release file...")
            time.sleep(0.5)

            self._write_safe(file_path, filename, cleaned_content)
            print(f"   ⏪ [ROLLBACK] Restored {filename} from {latest_backup} (Cleaned)")

        except Exception as e:
            print(f"   🛑 Rollback failed: {e}")

    def _write_safe(self, file_path, filename, content):
        content_hash = self._get_file_hash(content)
        self.last_hash[filename] = content_hash
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def _memorize(self, file_path, filename):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            self.memory.memorize(filename, text)
        except: pass