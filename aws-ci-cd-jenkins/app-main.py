import logging
import random
import os
from fastapi import FastAPI
from app.config import settings

# Ensure the log folder exists locally
os.makedirs(os.path.dirname(settings.LOG_FILE_PATH), exist_ok=True)

# Write logs straight to the local disk path
logging.basicConfig(
    filename=settings.LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Bare-Metal Production App Simulator")

ROUTES = ["/api/v1/users", "/api/v1/payments", "/dashboard", "/login"]
STATUS_CODES = [200, 200, 201, 404, 500]

@app.get("/")
def home():
    return {"status": "Application running natively on host instance."}

@app.get("/traffic")
def simulate_traffic():
    route = random.choice(ROUTES)
    status = random.choice(STATUS_CODES)
    log_message = f"Method=GET Route={route} Status={status}"
    
    if status >= 500:
        logging.error(log_message)
    elif status >= 400:
        logging.warning(log_message)
    else:
        logging.info(log_message)
        
    return {"route_visited": route, "response_status": status}
@app.get("/test-pipeline")
def test_pipeline():
    return {"status": "Success!", "message": "The Jenkins pipeline deployed this natively!"}
