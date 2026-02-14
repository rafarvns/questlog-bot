# Implementation Plan - Scribble Scribe (Path A)

Implement a transcription service for Questlog Bot that processes Craig's recordings, stores progress in PostgreSQL, and uses OpenAI's Whisper for high-quality transcription.

## Proposed Changes

### [Scribble Scribe Service]

#### [NEW] [implementation_plan.md](file:///e:/RANDOM/questlog-bot/services/scribble-scribe/implementation_plan.md)
Document the technical architecture and steps for the transcription service.

#### [MODIFY] [pyproject.toml](file:///e:/RANDOM/questlog-bot/services/scribble-scribe/pyproject.toml)
Add dependencies:
- `openai-whisper`
- `sqlalchemy` / `psycopg2-binary` (Database)
- `python-dotenv` (ENV management)
- `pydub` or `sub-process` for FFmpeg (Audio conversion)

#### [NEW] [.env.example](file:///e:/RANDOM/questlog-bot/services/scribble-scribe/.env.example)
Define environment variables:
- `DATABASE_URL`: PostgreSQL connection string.
- `WHISPER_MODEL`: Model size (tiny, base, small, medium, large).
- `WHISPER_DEVICE`: Device selection (cpu, cuda).
- `RECORDINGS_PATH`: Path to Craig's recording folder.

#### [NEW] [database.py](file:///e:/RANDOM/questlog-bot/services/scribble-scribe/database.py)
SQLAlchemy setup and models:
- `Transcription`: Stores ID, session name, status (pending, processing, completed), and full text.

#### [NEW] [transcriber.py](file:///e:/RANDOM/questlog-bot/services/scribble-scribe/transcriber.py)
Whisper logic:
- Load model based on ENV.
- Convert Craig's raw files to WAV using FFmpeg.
- Perform transcription per user track.

#### [MODIFY] [main.py](file:///e:/RANDOM/questlog-bot/services/scribble-scribe/main.py)
Service entry point:
- Monitor for new recordings.
- Orchestrate the conversion -> transcription -> storage flow.
- Generate formatted TXT output.

## Technical Details

### Transcription Format (TXT)
The service will generate a file named `sessão de voz X.txt` with the following pattern:
```text
> [Timestamp] | [Username]: [Transcribed Message]
```
Messages will be sorted chronologically.

### Database Integration
Every transcription session will be registered in PostgreSQL to allow future web application integration.
- Columns: `id` (PK), `session_id`, `user_id`, `content`, `timestamp`, `status`.

## Verification Plan

### Automated Tests
- Test database connection and migration.
- Mock Whisper transcription with a short audio sample.

### Manual Verification
- Run a recording with Craig.
- Trigger Scribble Scribe manually to check if the `.txt` and DB entries are correctly generated.
