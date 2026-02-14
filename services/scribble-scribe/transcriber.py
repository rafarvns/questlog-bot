import os
import whisper
import torch
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

class Transcriber:
    def __init__(self):
        self.model_name = os.getenv("WHISPER_MODEL", "base")
        self.device = os.getenv("WHISPER_DEVICE", "cpu")
        
        # Override device if CUDA is requested but not available
        if self.device == "cuda" and not torch.cuda.is_available():
            print("CUDA requested but not available. Falling back to CPU.")
            self.device = "cpu"
            
        print(f"Loading Whisper model '{self.model_name}' on {self.device}...")
        self.model = whisper.load_model(self.model_name, device=self.device)

    def transcribe(self, audio_path):
        """
        Transcribes a single audio file.
        Returns a list of segments with text and timestamps.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        result = self.model.transcribe(audio_path)
        return result['segments']

    def convert_to_wav(self, input_path, output_path):
        """
        Converts Ogg/Opus/FLAC to WAV (16kHz, mono) for better Whisper compatibility.
        """
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(output_path, format="wav")
        return output_path
