import time
import os
from watchdog.observers import Observer
from src.core.config import TARGET_FOLDER
from src.handlers.handler import OracleHandler
from src.utils.file_ops import ensure_workspace

if __name__ == "__main__":
    # Ensure the target folder exists
    ensure_workspace(TARGET_FOLDER)
    
    print("---------------------------------------------------")
    print(f"👁️  PYTHIA v2.0 (Refactored) IS ONLINE")
    print(f"📂 Watching: {TARGET_FOLDER}")
    print("---------------------------------------------------")

    event_handler = OracleHandler()
    observer = Observer()
    observer.schedule(event_handler, TARGET_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n💤 The Oracle sleeps.")
    observer.join()