import os
import time
from watchdog.events import FileSystemEventHandler
from src.memory import MemoryEngine
from src.brain import Brain

class OracleHandler(FileSystemEventHandler):
    def __init__(self):
        self.memory = MemoryEngine()
        self.brain = Brain()

    def on_moved(self, event):
        if event.is_directory: return
        self._handle_event(event.dest_path, event_type="created")

    def on_created(self, event):
        if event.is_directory: return
        time.sleep(0.5) # Wait for write
        self._handle_event(event.src_path, event_type="created")

    def on_modified(self, event):
        if event.is_directory: return
        self._handle_event(event.src_path, event_type="modified")

    def on_deleted(self, event):
        if event.is_directory: return
        
        filename = os.path.basename(event.src_path)
        # Check if it was a file we cared about
        valid_exts = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.sql']
        _, ext = os.path.splitext(filename)
        if ext.lower() in valid_exts:
            print(f"\n❌ [DELETED] '{filename}'")
            self.memory.forget(filename)

    def on_moved(self, event):
        if event.is_directory: return
        
        # A rename is actually two steps:
        # Step A: Forget the OLD name
        old_filename = os.path.basename(event.src_path)
        self.memory.forget(old_filename)

        # Step B: Learn the NEW name
        self._handle_event(event.dest_path, event_type="created")

    def _handle_event(self, file_path, event_type):
        filename = os.path.basename(file_path)
        
        # 1. Filter system files
        if filename.startswith(".") or filename.startswith("~"): return

        # This gives you time to rename "New Text Document.txt" to "main.py"
        if "New Text Document" in filename:
            return 
        
        # 2. Valid Extensions
        valid_exts = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.sql']
        _, ext = os.path.splitext(filename)
        if ext.lower() not in valid_exts: return

        try:
            if not os.path.exists(file_path): return
            size = os.path.getsize(file_path)
        except OSError:
            return

        # LOGIC: Empty File = Prompt. Full File = Memory.
        if size == 0 and event_type == "created":
            print(f"\n🔮 [PROMPT] '{filename}'")
            self._fulfill_prophecy(file_path, filename, ext)
        elif size > 0:
            # Avoid learning our own loading messages
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                if "The Oracle is" in f.read(50): return
            
            # Learn it
            print(f"\n🧠 [LEARNING] '{filename}'")
            self._memorize(file_path, filename)

    def _memorize(self, file_path, filename):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        self.memory.memorize(filename, text)

    def _fulfill_prophecy(self, file_path, filename, ext):
        # 1. Loading State
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("🔮 The Oracle is searching its memories...")

        # 2. Retrieve Context
        query = filename.replace("_", " ")
        print(f"   🔍 Searching memory for: '{query}'...")
        results = self.memory.recall(query)
        
        context_str = ""
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                source = results['metadatas'][0][i]['filename']
                context_str += f"\n--- MEMORY FROM {source} ---\n{doc}\n"
            print(f"   💡 Context found: {[m['filename'] for m in results['metadatas'][0]]}")
        else:
            print("   🌑 No context found. Running pure generation.")

        # 3. Generate
        content = self.brain.generate(filename, ext, context_str)

        # 4. Save
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ [SUCCESS] Written to {filename}")