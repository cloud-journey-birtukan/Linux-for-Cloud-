from fastapi import FastAPI, UploadFile, File, HTTPException
import httpx
import base64
import json

app = FastAPI()

@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    
    # 1. Prepare the data
    data = await file.read()
    encoded_image = base64.b64encode(data).decode('utf-8')

    payload_dict = {
        "filename": file.filename,
        "content_type": file.content_type,
        "content": encoded_image
    }

    # 2. Call the Worker directly via HTTP
    # The URL below is the EXACT 'front door' of the Lambda Emulator
    worker_url = "http://worker:8080/2015-03-31/functions/function/invocations"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(worker_url, json=payload_dict, timeout=60.0)
            
            if response.status_code != 200:
                # This will show you exactly what the worker is complaining about
                return {"status": "error", "worker_log": response.text}

            return {
                "status": "Success",
                "worker_response": response.json()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not connect to worker: {str(e)}")