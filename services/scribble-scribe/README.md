# Scribble Scribe ✍️🎙️

Scribble Scribe is the transcription service for the **Questlog Bot** ecosystem. It acts as a digital scribe, taking audio recordings captured by **Craig** and converting them into structured text.

## 🚀 Overview

The service processes raw multi-track audio data from Craig, transcribes it using OpenAI's **Whisper**, and stores the results both in a **PostgreSQL** database and in formatted `.txt` files.

### Key Features:
- **High-Quality Transcription**: Uses OpenAI Whisper with configurable models.
- **Hardware Acceleration**: Support for GPU (CUDA) execution via environment variables.
- **Structured Storage**: Saves every transcription session and individual message in PostgreSQL for web integration.
- **Chronological Output**: Generates a `.txt` file for each session with a consistent format:
  `> HH:MM:SS | Username: Transcribed Message`

## 🛠️ Requirements

- **Python**: 3.9 or higher.
- **FFmpeg**: Required for audio conversion (must be in your system PATH).
- **PostgreSQL**: An active instance for data storage.
- **GPU (Optional)**: NVIDIA GPU with CUDA drivers for faster transcription.

## ⚙️ Configuration

1. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. Configure the following variables:
   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `WHISPER_MODEL`: Model size (`tiny`, `base`, `small`, `medium`, `large`).
   - `WHISPER_DEVICE`: Set to `cuda` for GPU or `cpu`.
   - `RECORDINGS_PATH`: Path where Craig stores its `.data` and `.users` files.

## 🏃 How to Run

### 1. Setup Environment
Initialize the virtual environment and install dependencies:
```bash
# Using the existing .venv
.venv\Scripts\activate
# Dependencies are managed via pyproject.toml
pip install -e .
```

### 2. Initialize Database
The service automatically sets up its tables on startup if the database exists.

### 3. Start the Service
```bash
python main.py
```

## 📂 Project Structure

- `main.py`: Main orchestration and processing loop.
- `transcriber.py`: Whisper engine and audio conversion (FFmpeg) logic.
- `database.py`: SQLAlchemy models and PostgreSQL connection.
- `pyproject.toml`: Project metadata and dependencies.

## 📜 Transcription Format
Transcriptions are saved as `sessão de voz [SESSION_ID].txt` in the following format:
```text
> 14:05:12 | Legolas: I see a red sun rising.
> 14:05:30 | Gimli: My axe is ready!
```

---
*Developed as part of the Questlog Bot Monorepo.*
