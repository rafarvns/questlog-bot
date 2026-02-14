import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from database import SessionLocal, init_db, TranscriptionSession, Message
from transcriber import Transcriber

load_dotenv()

def process_recording(recording_id, recordings_path):
    """
    Main orchestration function for a single recording session.
    """
    db = SessionLocal()
    transcriber = Transcriber()
    
    file_base = os.path.join(recordings_path, recording_id)
    users_file = f"{file_base}.users"
    
    if not os.path.exists(users_file):
        print(f"Error: .users file not found for session {recording_id}")
        return

    # 1. Load users metadata
    with open(users_file, 'r') as f:
        # Craig .users is JSON-like per line
        raw_users = f.read().splitlines()
        users_map = {}
        for line in raw_users:
            if line.startswith(','):
                line = line[1:]
            try:
                data = json.loads("{" + line + "}")
                for track, info in data.items():
                    users_map[int(track)] = info
            except:
                continue

    # 2. Register session in DB
    session_name = f"sessão de voz {recording_id}"
    db_session = TranscriptionSession(session_name=session_name, status="processing")
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    # 3. Process tracks (Simulation of reconstructed audio files)
    # Note: Craig reconstruction logic will be implemented later.
    # For now, we assume WAV files are available per track.
    all_messages = []
    
    # Placeholder for logic that iterates over reconstructed user tracks
    # for track_no, user_info in users_map.items():
    #    ... conversion and transcription ...
    
    # 4. Save to TXT and DB
    output_txt_path = f"{session_name}.txt"
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        # Sort messages by timestamp
        all_messages.sort(key=lambda x: x['timestamp'])
        
        for msg in all_messages:
            formatted_msg = f"> {msg['timestamp'].strftime('%H:%M:%S')} | {msg['username']}: {msg['text']}\n"
            f.write(formatted_msg)
            
            # Save to DB
            db_msg = Message(
                session_id=db_session.id,
                username=msg['username'],
                content=msg['text'],
                timestamp=msg['timestamp'],
                track_no=msg['track_no']
            )
            db.add(db_msg)

    db_session.status = "completed"
    db.commit()
    print(f"Transcription for {recording_id} completed.")

def main():
    print("Scribble Scribe starting...")
    # try:
    #     init_db()
    # except Exception as e:
    #     print(f"Database initialization failed: {e}. Check your DATABASE_URL.")
    
    # TODO: Implement file system watcher or polling logic
    print("Ready to process recordings.")

if __name__ == "__main__":
    main()
