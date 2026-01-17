import time
from watchdog.observers import Observer
from src.config import TARGET_FOLDER
from src.handler import OracleHandler

if __name__ == "__main__":
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