# Image Processing Service

This is a FastAPI application for uploading images, compressing them, and storing a simple in-memory processing history.

## Setup

Install the required packages:

```bash
pip install fastapi uvicorn pillow python-multipart
```

## Run

From the `webapp` directory:

```bash
python3 main.py
```

Or run with Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

- `POST /api/v1/images/upload` uploads and compresses an image.
- `GET /api/v1/history` returns processing history.
- `GET /api/v1/health` checks service status.

## Test Commands

Test in Swagger UI:

1. Start the app and open `http://127.0.0.1:8000/docs`.
2. Open `POST /api/v1/images/upload`.
3. Click `Try it out`.
4. Choose an image file in the `file` field.
5. Click `Execute`.
6. Open `GET /api/v1/history` and click `Execute` to confirm the upload was saved in history.
7. Open `GET /api/v1/health` and click `Execute` to check the service status.

Upload an image:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/images/upload" \
  -F "file=@/path/to/image.png"
```

Get history:

```bash
curl "http://127.0.0.1:8000/api/v1/history?limit=10&offset=0"
```

Health check:

```bash
curl "http://127.0.0.1:8000/api/v1/health"
```

## Notes

- Supported image types: JPG, JPEG, PNG, GIF, BMP, WEBP.
- Maximum file size: `10MB`.
- History is stored in memory only, so it resets when the server restarts.
