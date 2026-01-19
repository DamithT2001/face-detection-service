"""Integration tests for API endpoints."""

import io
import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_returns_healthy(self):
        """Should return healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestDetectEndpoint:
    """Tests for face detection endpoint."""

    def test_detect_rejects_non_image_content_type(self):
        """Should reject files with non-image content type."""
        response = client.post(
            "/api/face-detect",
            files={"image": ("test.txt", b"not an image", "text/plain")},
        )
        assert response.status_code == 400
        assert "image" in response.json()["detail"].lower()

    def test_detect_handles_invalid_image_gracefully(self):
        """Should handle corrupted/invalid image data."""
        response = client.post(
            "/api/face-detect",
            files={"image": ("test.jpg", b"invalid data", "image/jpeg")},
        )
        assert response.status_code == 200
        assert response.json()["face_detected"] is False
