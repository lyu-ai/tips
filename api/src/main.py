from fastapi import FastAPI, Request
import uvicorn
import logging
from api.v1.endpoints import audio
from websocket import audio_socket
from fastapi.middleware.cors import CORSMiddleware

logging.debug("Imports completed...")
logging.basicConfig(level=logging.DEBUG)
logging.debug("Starting application...")

app = FastAPI()


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.debug(f"Received request: {request.method} {request.url}")
    logging.debug(f"Headers: {request.headers}")
    response = await call_next(request)
    return response


# Register API routers
app.include_router(audio.router, prefix="/api/v1/audio", tags=["audio"])
# app.include_router(image.router, prefix="/api/v1/image", tags=["image"])
# app.include_router(video.router, prefix="/api/v1/video", tags=["video"])

# Register WebSocket routers
app.include_router(audio_socket.router, tags=["audio_ws"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Armstrong Perception Services!"}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8842, reload=True)


if __name__ == "__main__":
    main()
