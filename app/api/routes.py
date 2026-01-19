"""API routes for face detection."""

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.schemas import FaceDetectionResponse
from app.services.detector import get_detector

router = APIRouter()


@router.post("/face-detect", response_model=FaceDetectionResponse)
async def detect_face(image: UploadFile = File(...)) -> FaceDetectionResponse:
    """Detect if a human face is present in the uploaded image.
    
    Args:
        image: Image file to analyze.
        
    Returns:
        FaceDetectionResponse with face_detected boolean.
    """
    # Validate content type
    if image.content_type and not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image bytes
    image_bytes = await image.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    # Detect face
    detector = get_detector()
    face_detected = detector.detect(image_bytes)

    return FaceDetectionResponse(face_detected=face_detected)
