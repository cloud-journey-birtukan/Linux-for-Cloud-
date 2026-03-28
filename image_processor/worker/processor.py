import os
import boto3
import base64
import json
import time
from io import BytesIO
from PIL import Image, ImageOps # Added ImageOps for extra processing

# 1. YOUR REAL BUCKET CONFIG
BUCKET_NAME = "amzn-for-demo" 
REGION = "eu-north-1" 

# Initialize S3 Client
s3 = boto3.client(
    's3',
    region_name=REGION,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def lambda_handler(event, context):
    try:
        filename = event.get('filename', 'image.jpg')
        content_type = event.get('content_type', 'image/jpeg')
        encoded_content = event.get('content')

        if not encoded_content:
            return {"error": "No image content provided"}

        # --- ACTUAL IMAGE PROCESSING LOGIC START ---
        
        # 1. Load the image from the Base64 data
        image_data = base64.b64decode(encoded_content)
        img = Image.open(BytesIO(image_data))
        
        # 2. Convert to Grayscale (Black & White)
        # This makes it obvious that the "Processor" actually did something!
        img = ImageOps.grayscale(img)
        
        # 3. Resize to a standard size (e.g., 800x800)
        img.thumbnail((800, 800))
        
        # 4. Save the processed image to a buffer
        buffer = BytesIO()
        img_format = 'PNG' if 'png' in content_type.lower() else 'JPEG'
        img.save(buffer, format=img_format)
        buffer.seek(0)
        
        # --- ACTUAL IMAGE PROCESSING LOGIC END ---

        # 5. Upload to your bucket
        target_key = f"processed/{int(time.time())}_{filename}"
        
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=target_key,
            Body=buffer,
            ContentType=content_type
        )

        return {
            "statusCode": 200,
            "body": {
                "message": "Image converted to Grayscale and uploaded!",
                "target_key": target_key,
                "bucket": BUCKET_NAME
            }
        }

    except Exception as e:
        print(f"Error detail: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"Processing logic failed: {str(e)}"
        }

async def app(scope, receive, send):
    if scope['type'] == 'http':
        message = await receive()
        body = message.get('body', b'{}')
        try:
            payload = json.loads(body)
        except:
            payload = {}

        class FakeContext:
            aws_request_id = "local_run"

        result = lambda_handler(payload, FakeContext())

        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'application/json']],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(result).encode('utf-8'),
        })

if __name__ == "__main__":
    import uvicorn
    print(f"Worker active. Using bucket: {BUCKET_NAME}")
    uvicorn.run(app, host="0.0.0.0", port=8080)