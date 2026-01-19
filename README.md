# Face Detection Service

A REST API for detecting human faces in images using MediaPipe.

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## API

### POST /api/face-detect

Detects if a human face is present in the uploaded image.

**Request:** Form-data with `image` file

**Response:**
```json
{
  "face_detected": true
}
```

### GET /health

Health check endpoint.

## Test

```bash
pytest tests/
```
