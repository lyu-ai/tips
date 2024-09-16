import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_audio_websocket():
    with client.websocket_connect("/ws/audio") as websocket:
        # Simulate sending audio data
        audio_data = b"\x00\x01\x02"  # Example byte data
        websocket.send_bytes(audio_data)

        # Receive the processing result
        result = websocket.receive_json()

        # Assertions to validate the result
        assert "transcript" in result
        assert "emotion" in result
