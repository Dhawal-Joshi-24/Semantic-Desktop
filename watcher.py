import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import our Shredder
from processor import DocumentProcessor

class DocumentHandler(FileSystemEventHandler):
    def __init__(self):
        self.processor = DocumentProcessor()
        # A dictionary to remember when we last processed a file
        self.last_processed = {} 

    def safe_process(self, file_path):
        """The 'Debouncer' - Prevents Windows from spamming duplicate events"""
        current_time = time.time()
        last_time = self.last_processed.get(file_path, 0)
        
        # If we processed this exact file less than 2 seconds ago, ignore it!
        if current_time - last_time < 2:
            return 
            
        # Update the timestamp
        self.last_processed[file_path] = current_time
        
        # Wait 1 second for Windows to finish saving and release the file lock
        time.sleep(1) 
        
        # Send to the shredder!
        self.processor.process_file(file_path)

    def on_created(self, event):
        if not event.is_directory:
            print(f"\n✨ File creation caught: {event.src_path}")
            self.safe_process(event.src_path)
            
    def on_modified(self, event):
        if not event.is_directory:
            print(f"🔄 File modification caught: {event.src_path}")
            self.safe_process(event.src_path)

if __name__ == "__main__":
    path = "./my_documents"
    
    if not os.path.exists(path):
        os.makedirs(path)

    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print(f"🚀 Semantic Watcher started on: {path}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Watcher stopped.")
    observer.join()