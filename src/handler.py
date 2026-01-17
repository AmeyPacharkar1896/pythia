import os
import time
from watchdog.events import FileSystemEventHandler
from src.memory import MemoryEngine
from src.brain import Brain

class OracleHandler(FileSystemEventHandler):
    def __init__(self):
        self.memory = MemoryEngine()
        self.brain = Brain()

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
        valid_exts = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.sql']
        _, ext = os.path.splitext(filename)
        if ext.lower() in valid_exts:
            print(f"\n❌ [DELETED] '{filename}'")
            self.memory.forget(filename)

    def on_moved(self, event):
        if event.is_directory: return
        
        # Step A: Forget the OLD name
        old_filename = os.path.basename(event.src_path)
        self.memory.forget(old_filename)

        # Step B: Learn the NEW name
        self._handle_event(event.dest_path, event_type="created")

    def _handle_event(self, file_path, event_type):
        filename = os.path.basename(file_path)
        
        # 1. Filter system files
        if filename.startswith(".") or filename.startswith("~"): return
        if "New Text Document" in filename: return 
        
        # 2. Valid Extensions
        valid_exts = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.sql', '.mermaid']
        _, ext = os.path.splitext(filename)
        if ext.lower() not in valid_exts: return

        try:
            if not os.path.exists(file_path): return
            size = os.path.getsize(file_path)
        except OSError:
            return

        # LOGIC: Empty File = Prompt. Full File = Memory/Edit.
        if size == 0 and event_type == "created":
            if ext == ".mermaid":
                # 1. Find the source code file with the same name
                source_file = None
                folder = os.path.dirname(file_path)
                base_name = os.path.splitext(filename)[0] # e.g. "Find_Treasure_v2"
                
                # Check for matching code files
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
                    print(f"   Make sure a file like '{base_name}.py' exists.")

            else:
                # Normal Generation
                print(f"\n🔮 [PROMPT] '{filename}'")
                self._fulfill_prophecy(file_path, filename, ext)
        
        elif size > 0:
            if ext == ".mermaid": return
            try:
                # 🟢 FIXED: The Try block now has logic and an except block
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Safety check
                if "The Oracle is" in content[:100]: return

                # Check for "UPDATE:" command
                lines = content.strip().split('\n')
                last_line = lines[-1].strip() if lines else ""

                if "UPDATE:" in last_line:
                    print(f"\n✨ [EDIT REQUEST] Detected command in '{filename}'")
                    print(f"   📝 Instruction: {last_line}")
                    self._perform_edit(file_path, filename, ext, content, last_line)
                else:
                    print(f"\n🧠 [LEARNING] '{filename}'")
                    self._memorize(file_path, filename)
            
            except Exception as e:
                print(f"Error processing file: {e}")

    def _perform_edit(self, file_path, filename, ext, content, instruction):
        """Helper to run the refactoring logic."""
        # 1. Ask Brain to Refactor
        new_content = self.brain.refactor(filename, ext, content, instruction)
        
        # 2. Overwrite the file with the NEW version
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"✅ [SUCCESS] Refactored {filename}")
        # We don't memorize here; the next 'on_modified' event will handle memorization automatically

    def _memorize(self, file_path, filename):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            self.memory.memorize(filename, text)
        except:
            pass

    def _fulfill_prophecy(self, file_path, filename, ext):
        try:
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
        except Exception as e:
            print(f"🛑 Generation Error: {e}")

    def _generate_diagram(self, diagram_path, source_path):
        try:
            # 1. Read the source code
            with open(source_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            # 2. Ask Brain to Visualize
            diagram_code = self.brain.visualize(os.path.basename(source_path), code_content)

            # 3. Save the Mermaid file
            with open(diagram_path, 'w', encoding='utf-8') as f:
                f.write(diagram_code)
            
            print(f"✅ [SUCCESS] Diagram generated: {os.path.basename(diagram_path)}")
        except Exception as e:
            print(f"🛑 Error: {e}")