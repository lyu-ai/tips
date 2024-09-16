from fastapi import APIRouter, UploadFile, File, HTTPException
from services.audio_service import process_audio_stream

router = APIRouter()


@router.get("/process_audio")
async def read_root():
    return {"message": "API exists!"}


@router.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Read audio data
        audio_data = await file.read()

        # Call the service to process the audio data
        result = process_audio_stream(audio_data)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
