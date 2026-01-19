"""Pydantic schemas for API request/response models."""

from pydantic import BaseModel


class FaceDetectionResponse(BaseModel):
    """Response model for face detection endpoint."""

    face_detected: bool
