import numpy as np
from transformers import pipeline
import librosa

# Initialize the ASR model pipeline (without specifying sampling rate here)
asr_pipeline = pipeline(
    "automatic-speech-recognition", model="facebook/wav2vec2-base-960h"
)


def pad_audio(audio_data: np.ndarray, target_length: int) -> np.ndarray:
    """
    Pads the audio data with silence (zeros) if it is shorter than the target length.
    :param audio_data: numpy array of audio data
    :param target_length: target length in samples (e.g., 16000 for 1 second of 16kHz audio)
    :return: padded audio data
    """
    if len(audio_data) < target_length:
        pad_length = target_length - len(audio_data)
        padded_audio = np.pad(audio_data, (0, pad_length), mode="constant")
        return padded_audio
    return audio_data


def process_audio_stream(data: bytes) -> dict:
    try:
        # Convert raw PCM data to numpy array (assuming float32 format)
        audio_data = np.frombuffer(data, dtype=np.float32)

        # Resample the audio to 16kHz if necessary (you can adjust this as per your source sample rate)
        audio_data_resampled = librosa.resample(
            audio_data, orig_sr=44100, target_sr=16000
        )

        # Ensure the audio is mono (1 channel)
        if audio_data_resampled.ndim > 1:
            audio_data_resampled = np.mean(audio_data_resampled, axis=1)

        # Pad the audio to at least 1 second (16k samples for 16kHz audio)
        target_length = 16000  # 1 second of audio at 16kHz
        audio_data_padded = pad_audio(audio_data_resampled, target_length)

        # Send the padded audio to the ASR pipeline
        asr_result = asr_pipeline(audio_data_padded)
        transcript = asr_result.get("text", "")

        # Perform emotion recognition (placeholder)
        emotion_result = {"emotion": "neutral", "confidence": 1.0}

        return {
            "transcript": transcript,
            "emotion": emotion_result["emotion"],
            "emotion_confidence": emotion_result["confidence"],
        }
    except Exception as e:
        return {"error": str(e)}
