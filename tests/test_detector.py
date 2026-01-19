"""Unit tests for FaceDetector service."""

import pytest
from app.services.detector import FaceDetector


class TestFaceDetector:
    """Tests for FaceDetector class."""

    def test_detect_returns_false_for_invalid_image(self):
        """Should return False for invalid image bytes."""
        detector = FaceDetector()
        result = detector.detect(b"not an image")
        assert result is False
        detector.close()

    def test_detect_returns_false_for_empty_bytes(self):
        """Should return False for empty bytes."""
        detector = FaceDetector()
        result = detector.detect(b"")
        assert result is False
        detector.close()
