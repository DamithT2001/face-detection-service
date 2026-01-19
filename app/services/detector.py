"""Face detection service using MediaPipe."""

import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Path to the model file
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "blaze_face_short_range.tflite")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Face detection model not found at {MODEL_PATH}. "
        "Download blaze_face_short_range.tflite and place it in the project root."
    )


class FaceDetector:
    """Detects human faces in images using MediaPipe Face Detection."""

    def __init__(self, min_confidence: float = 0.5):
        """Initialize the face detector.
        
        Args:
            min_confidence: Minimum confidence threshold for detection (0.0 to 1.0).
        """
        self._min_confidence = min_confidence
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.FaceDetectorOptions(
            base_options=base_options,
            min_detection_confidence=self._min_confidence,
        )
        self._detector = vision.FaceDetector.create_from_options(options)

    def detect(self, image_bytes: bytes) -> bool:
        """Detect if a human face is present in the image.
        
        Args:
            image_bytes: Raw image bytes.
            
        Returns:
            True if at least one face is detected, False otherwise.
        """
        if not image_bytes:
            return False

        # Decode image bytes to numpy array
        np_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            return False

        # Convert BGR to RGB (MediaPipe expects RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        # Process the image
        results = self._detector.detect(mp_image)

        # Check if any faces were detected (results.detections may be None)
        detections = getattr(results, "detections", None)
        return bool(detections)

    def close(self) -> None:
        """Release resources."""
        self._detector.close()


# Singleton instance for reuse
_detector: FaceDetector | None = None


def get_detector() -> FaceDetector:
    """Get the singleton face detector instance."""
    global _detector
    if _detector is None:
        _detector = FaceDetector()
    return _detector


def close_detector() -> None:
    """Close and clear the singleton detector instance."""
    global _detector
    if _detector is not None:
        _detector.close()
        _detector = None
