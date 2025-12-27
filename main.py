# main.py
from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
from pydantic import BaseModel
from typing import Optional
import logging
import uvicorn
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Client Info API", description="Captures IP and location. Can receive uploaded images.")

# --- Data Models ---
class ClientInfo(BaseModel):
    """Model for IP and geolocation data."""
    ip_address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    isp: Optional[str] = None
    error: Optional[str] = None

class ClientInfoWithImage(BaseModel):
    """Model combining client info and image metadata."""
    client_info: ClientInfo
    image_filename: Optional[str] = None
    image_size: Optional[int] = None
    upload_error: Optional[str] = None

# --- Core Geolocation Function ---
async def get_ip_geolocation(ip: str) -> dict:
    """
    Fetches geolocation data from ipinfo.io.
    SIGNUP REQUIRED: Get a free token at https://ipinfo.io/signup
    """
    API_TOKEN = os.getenv("API_TOKEN")
    if API_TOKEN == os.getenv("API_TOKEN") is None:
        return {"error": "Server configuration error: API token not set."}
    
    url = f"https://ipinfo.io/{ip}/json?token={API_TOKEN}"
    
    try:
        async with httpx.AsyncClient() as client:
            # 5-second timeout for the external API call
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        logger.warning(f"Geolocation API timeout for IP: {ip}")
        return {"error": "Geolocation service timed out."}
    except httpx.HTTPStatusError as e:
        logger.error(f"Geolocation API HTTP error: {e.response.status_code} for IP: {ip}")
        return {"error": f"Geolocation service error: {e.response.status_code}"}
    except Exception as e:
        logger.error(f"Unexpected error during geolocation: {e} for IP: {ip}")
        return {"error": "Could not fetch geolocation data."}

async def capture_client_info_from_request(request: Request) -> ClientInfo:
    """
    Extracts IP and geolocation data from a FastAPI request.
    """
    # 1. Get the client's IP address (handles proxies)
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # Get the first IP in the chain (the original client)
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else None
    
    if not client_ip or client_ip == "127.0.0.1":
        return ClientInfo(
            ip_address=client_ip,
            error="Could not determine a valid public IP address."
        )
    
    # 2. Fetch geolocation data
    geo_data = await get_ip_geolocation(client_ip)
    
    if "error" in geo_data:
        return ClientInfo(ip_address=client_ip, error=geo_data["error"])
    
    # 3. Parse and return structured data
    return ClientInfo(
        ip_address=client_ip,
        country=geo_data.get("country"),
        city=geo_data.get("city"),
        region=geo_data.get("region"),
        isp=geo_data.get("org")  # 'org' field from ipinfo.io contains ISP info
    )

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def root():
    """Simple homepage with instructions."""
    return """
    <html>
        <head><title>Client Info API</title></head>
        <body>
            <h1>Client Info API is Running</h1>
            <p>Endpoints:</p>
            <ul>
                <li><strong>GET /capture-info</strong>: Returns IP and geolocation as JSON.</li>
                <li><strong>POST /upload-image/</strong>: Accepts an image file along with IP data. Use multipart/form-data.</li>
                <li><a href="/docs">Interactive API Docs (Swagger UI)</a></li>
            </ul>
            <p><em>Note: This API cannot remotely access user cameras. Any image must be uploaded by the user.</em></p>
        </body>
    </html>
    """

@app.get("/capture-info", response_model=ClientInfo)
async def capture_info(request: Request):
    """
    Primary endpoint. Returns the caller's IP address and geolocation data.
    """
    return await capture_client_info_from_request(request)

@app.post("/upload-image/", response_model=ClientInfoWithImage)
async def upload_image_with_info(
    request: Request,
    file: Optional[UploadFile] = File(None)
):
    """
    Endpoint that captures client info AND accepts an optional uploaded image.
    This simulates what a frontend app could do after getting camera permission.
    """
    # 1. Capture IP and geolocation data
    client_info = await capture_client_info_from_request(request)
    
    result = ClientInfoWithImage(client_info=client_info)
    
    # 2. Process the uploaded image if present
    if file and file.filename:
        # Validate it's an image (basic check)
        if not file.content_type.startswith("image/"):
            result.upload_error = f"File '{file.filename}' is not an image. Type: {file.content_type}"
            logger.warning(result.upload_error)
        else:
            try:
                # Read the file to get its size (in a real app, you'd save it)
                contents = await file.read()
                result.image_filename = file.filename
                result.image_size = len(contents)
                logger.info(f"Received image: {file.filename} ({result.image_size} bytes) from IP: {client_info.ip_address}")
                # In production: save contents to disk/cloud storage here
                # with open(f"uploads/{file.filename}", "wb") as f:
                #     f.write(contents)
            except Exception as e:
                result.upload_error = f"Failed to process image: {str(e)}"
                logger.error(f"Image processing error: {e}")
    else:
        result.upload_error = "No image file provided."
    
    return result

# --- Server Startup (for development) ---
if __name__ == "__main__":
    # The '--forwarded-allow-ips="*"' flag is CRUCIAL for correct IP detection when deployed.
    # This tells Uvicorn to trust forwarded headers from proxies.
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,
        reload=True,      # Auto-restart on code changes (development only)
        forwarded_allow_ips="*"  # IMPORTANT: Trust all forwarding proxies
    )