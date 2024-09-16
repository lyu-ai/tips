from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.audio_service import process_audio_stream

router = APIRouter()

active_connections: set[WebSocket] = set()


@router.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            # Try receiving the audio data
            try:
                data = await websocket.receive_bytes()

                # Process the audio stream (e.g., ASR, emotion analysis)
                result = process_audio_stream(
                    data
                )  # No need to await if this is a regular function

                # Send back the analysis results
                if result.get("transcript") != "":
                    await websocket.send_json(result)

            except WebSocketDisconnect:
                print("Client disconnected")
                break  # Exit the loop and clean up after disconnection

            except Exception as e:
                print(f"Error processing audio stream: {e}")
                await websocket.close(code=1000)
                break

    finally:
        active_connections.remove(websocket)
        try:
            if not websocket.client_state.closed:  # Only close if still open
                await websocket.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")
