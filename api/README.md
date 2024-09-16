# API

## Folder

Explanation of Each Folder

1. api/:

- Contains all your FastAPI route definitions and logic.
- Organized under v1/ for versioning (e.g., /api/v1/audio, /api/v1/image).
- Each file (like audio.py, image.py, video.py) defines endpoints for each specific task (ASR, emotion analysis, gesture recognition).

2. core/:

- Houses core configurations, security, and settings for the application.
- Example: managing environment variables, defining security (JWT, OAuth2), and other app-level configurations.

3. models/:

- Contains Pydantic models (data validation and request/response schemas) or ORM models (if you’re using databases like SQLAlchemy).

4. services/:

- Business logic for handling the core functionality of the application.
- Example: audio_service.py contains logic for handling ASR and emotion analysis, while image_service.py does age, gender, and emotion detection from images.

5. db/:

- Handles database configurations and interactions (e.g., using SQLAlchemy).
- base.py can have database engine and ORM base setup.
- Only necessary if your project is using a database.

6. utils/:

- Contains utility functions, like file handling, logging, or other reusable code that doesn’t fit into business logic or API routes.

7. tests/:

- Holds unit tests and integration tests to ensure everything functions as expected.

8. main.py:

- The main entry point of your FastAPI app, which ties together the API routes and other configurations.
- You’d import the routers defined in api/ here and include them in the main FastAPI instance.
