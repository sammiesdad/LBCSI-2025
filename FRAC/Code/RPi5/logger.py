import os
import hashlib
from datetime import datetime, timedelta

class TextLogger:
    def __init__(self, log_dir="logs", retention_days=30):
        self.log_dir = log_dir
        self.retention_days = retention_days
        os.makedirs(log_dir, exist_ok=True)
        self.date_str = datetime.now().strftime('%Y-%m-%d')
        self.log_filename = os.path.join(self.log_dir, f"log_{self.date_str}.txt")
        self._purge_old_logs()

    def log_event(self, event: str, uid: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} | UID: {uid} | EVENT: {event}"
        log_hash = self._hash_entry(log_entry)
        full_entry = f"{log_entry} | HASH: {log_hash}"

        print(full_entry)  # Optional console output

        with open(self.log_filename, "a") as f:
            f.write(full_entry + "\n")

    def _hash_entry(self, entry: str) -> str:
        return hashlib.sha256(entry.encode('utf-8')).hexdigest()

    def _purge_old_logs(self):
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)

        for filename in os.listdir(self.log_dir):
            if filename.startswith("log_") and filename.endswith(".txt"):
                date_str = filename[4:-4]  # Extract date part
                try:
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if file_date < cutoff_date:
                        file_path = os.path.join(self.log_dir, filename)
                        os.remove(file_path)
                        print(f"[INFO] Purged old log: {file_path}")
                except ValueError:
                    continue  # Skip unexpected formats


#Example Usage
#from text_logger import TextLogger

#logger = TextLogger(retention_days=30)

#logger.log_event("User login", uid="user123")
#logger.log_event("File uploaded", uid="user456")
#logger.log_event("Session ended", uid="user123")
