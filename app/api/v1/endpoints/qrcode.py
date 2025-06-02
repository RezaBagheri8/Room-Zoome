from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/qrcode",
    tags=["qrcode"]
)

class URLRequest(BaseModel):
    url: str

@router.post("/generate")
async def generate_qr_code(url_request: URLRequest):
    """Generate a QR code from a given URL and return it as an image"""
    try:
        # Generate QR code
        qr = qrcode.make(url_request.url)
        img_byte_arr = BytesIO()
        qr.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))