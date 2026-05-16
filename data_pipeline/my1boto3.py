import boto3 
import os 
import logging
import json
import threading # Added for the Lock
from dotenv import load_dotenv
from botocore.exceptions import ClientError, NoCredentialsError
from concurrent.futures import ThreadPoolExecutor
from botocore.config import Config

# --- CONFIGURATION ---
Tracker_File = "uploaded_metadata.json"
log_path = 'data_pipeline.log' 
history_lock = threading.Lock() 

logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger() 

load_dotenv() 

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("REGION_NAME")
s3_bucket = os.getenv("S3_BUCKET")
s3_folder = os.getenv("S3_FOLDER")

# Fix: Corrected retry config syntax
config = Config(
   retries = { 
       "max_attempts": 10,
       "mode": "standard" 
   }
)

s3 = boto3.resource(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
    config=config
)

# --- FUNCTIONS ---

def load_history():
    if os.path.exists(Tracker_File):
        with open(Tracker_File, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_history(history):
 with open(Tracker_File, 'w') as f:
        json.dump(list(history), f)

def check_and_upload_file(file_name, history):
    # Skip if file was already uploaded
    if file_name in history:
        print(f"Skipping: {file_name} already exists in history.")
        return

    # Skip folders or specific system files
    if not os.path.isfile(file_name) or file_name in [Tracker_File, '.env', 'my1boto3.py']:
        return

    success = False
    # Corrected S3 Path logic
    clean_folder = s3_folder.strip("/") if s3_folder else ""
    s3_path = f"{clean_folder}/{file_name}" if clean_folder else file_name

    try:
        print(f"Uploading {file_name}...")
        s3.Bucket(s3_bucket).upload_file(file_name, s3_path)
        s3.Object(s3_bucket, s3_path).wait_until_exists()
        logger.info(f"Successfully uploaded: {file_name}")
        success = True
    except Exception as e:
        logger.error(f"Error uploading {file_name}: {e}")

    if success:
        with history_lock:
            history.add(file_name)
def run_pipeline(target_directory):
    history = load_history()
    
    # 1. Check if the directory actually exists
    if not os.path.exists(target_directory):
        logger.error(f"Directory {target_directory} does not exist!")
        return

    # 2. Get the full paths for every file in that directory
    all_files = [
        os.path.join(target_directory, f) 
        for f in os.listdir(target_directory)
    ]
    
    # 3. Filter out things that are folders or blacklisted
    files_to_process = [f for f in all_files if os.path.isfile(f)]

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Each worker gets a full path from our list
        executor.map(lambda f: check_and_upload_file(f, history), files_to_process)
    
    save_history(history)

if __name__ == "__main__":
    # Specify your target folder here
    MY_DIR = "/home/birtukan/files_upload"
    run_pipeline(MY_DIR)
