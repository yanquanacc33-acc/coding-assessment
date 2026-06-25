import io
import uuid
import uvicorn
from datetime import datetime
from typing import List, Tuple

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import asyncio

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_HISTORY_RECORDS = 500
COMPRESSION_QUALITY = 80
MAX_IMAGE_DIMENSION = 2048
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'}

class ProcessingStatus:
    SUCCESSFUL = "successful"
    FAILED = "failed"

class ImageProcessResponse(BaseModel):
    id: str
    filename: str
    original_size: int
    compressed_size: int
    compression_ratio: float
    status: str
    timestamp: datetime
    error_message: str | None = None

class HistoryResponse(BaseModel):
    total: int
    records: List[ImageProcessResponse]

app = FastAPI()
history_records: List[ImageProcessResponse] = []

def validate_image(file: UploadFile) -> Tuple[str, bytes]:
    if not file.filename:
        raise HTTPException(400, "No filename provided")
    
    ext = ''
    if '.' in file.filename:
        ext = '.' + file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, f"Invalid MIME type: {file.content_type}")
    
    try:
        content = file.file.read()
    except Exception as e:
        raise HTTPException(400, f"Failed to read file: {str(e)}")
    
    if len(content) > MAX_FILE_SIZE:
        max_size_mb = MAX_FILE_SIZE // (1024*1024)
        raise HTTPException(400, f"File too large. Max: {max_size_mb}MB")
    
    return file.filename, content

def compress_image(content: bytes) -> Tuple[bytes, int]:
    try:
        image = Image.open(io.BytesIO(content))
        
        # Handle transparency
        if image.mode in ('RGBA', 'LA', 'P'):
            if image.mode == 'P':
                image = image.convert('RGBA')
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[3])
            elif image.mode == 'LA':
                background.paste(image, mask=image.split()[1])
            image = background
        
        # Resize if too large
        if max(image.size) > MAX_IMAGE_DIMENSION:
            ratio = MAX_IMAGE_DIMENSION / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save compressed
        output = io.BytesIO()
        image_format = 'JPEG'
        if image.format and image.format.upper() in ('PNG', 'GIF', 'WEBP'):
            image_format = image.format.upper()
        
        save_kwargs = {'quality': COMPRESSION_QUALITY, 'optimize': True}
        if image_format == 'PNG':
            save_kwargs.pop('quality', None)
            save_kwargs['compress_level'] = 6
        elif image_format == 'GIF':
            save_kwargs.pop('quality', None)
        
        image.save(output, format=image_format, **save_kwargs)
        return output.getvalue(), len(output.getvalue())
        
    except Exception as e:
        raise HTTPException(500, f"Image processing failed: {str(e)}")

def add_history_record(filename: str, original_size: int, compressed_size: int, 
                       compression_ratio: float, status: str, 
                       error_message: str | None = None) -> ImageProcessResponse:
    global history_records
    
    record = ImageProcessResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        original_size=original_size,
        compressed_size=compressed_size,
        compression_ratio=compression_ratio,
        status=status,
        timestamp=datetime.utcnow(),
        error_message=error_message
    )
    
    history_records.append(record)
    
    if len(history_records) > MAX_HISTORY_RECORDS:
        history_records = history_records[-MAX_HISTORY_RECORDS:]
    
    return record

# API endpoints
@app.post("/api/v1/images/upload", response_model=ImageProcessResponse)
async def upload_and_compress_image(file: UploadFile = File(...)):
    
    try:
        filename, content = validate_image(file)
        original_size = len(content)
        
        compressed_content, compressed_size = await asyncio.to_thread(compress_image, content)
        if original_size > 0:
        compression_ratio = round(compressed_size / original_size, 4)
        
        # Save to history
        record = add_history_record(
            filename=filename,
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio,
            status=ProcessingStatus.SUCCESSFUL
        )
        
        return record
        
    except HTTPException as e:
        # Record failure
        add_history_record(
            filename=filename
            original_size=0,
            compressed_size=0,
            compression_ratio=0,
            status=ProcessingStatus.FAILED,
            error_message=e.detail
        )
        raise e
    except Exception as e:
        raise HTTPException(500, f"Internal error: {str(e)}")

@app.get("/api/v1/history", response_model=HistoryResponse)
async def get_history(
    limit: int | None = Query(50, ge=1, le=100),
    offset: int | None = Query(0, ge=0)
):
    records = history_records[::-1]
    
    if offset:
        records = records[offset:]
    if limit:
        records = records[:limit]
    
    return HistoryResponse(
        total=len(history_records),
        records=records
    )

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "total_processed": len(history_records)}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )