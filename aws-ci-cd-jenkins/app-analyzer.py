import time
import os
from app.config import settings

def tail_file(filename):
    """Watches the native file system log for append events"""
    while not os.path.exists(filename):
        print(f"Waiting for log file to be generated at: {filename}...")
        time.sleep(2)
        
    with open(filename, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line

def run_analyzer():
    print(f"Log Analyzer actively parsing: {settings.LOG_FILE_PATH}")
    error_counter = 0
    start_time = time.time()

    for log_line in tail_file(settings.LOG_FILE_PATH):
        if "Status=500" in log_line:
            error_counter += 1
            print(f"[ANOMALY LOGGED] Internal Error Counter: {error_counter}")

        if time.time() - start_time > 30:
            error_counter = 0
            start_time = time.time()

        if error_counter >= settings.ALERT_THRESHOLD:
            print(f"🚨 [ALERT] SYSTEM WARNING: {error_counter} critical errors hit within 30s!")
            error_counter = 0 

if __name__ == "__main__":
    run_analyzer()
