from dataclasses import dataclass
from typing import Dict, List, Tuple
import requests
import time
import os
from dotenv import load_dotenv

@dataclass
class AudioSegment:
    start_ms: int
    end_ms: int
    text: str
    topics: List[str]
    sentiment: str
    confidence: float

class AudioAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        if not self.api_key:
            raise ValueError("AssemblyAI API key not found in environment variables")

        self.base_url = "https://api.assemblyai.com/v2"
        self.headers = {
            "authorization": self.api_key
        }

    def _upload_file(self, file_path: str) -> str:
        """Upload a local file to AssemblyAI"""
        print(f"Uploading file to AssemblyAI: {file_path}")

        def read_file(file_path):
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(5242880)  # Read in 5MB chunks
                    if not data:
                        break
                    yield data

        # Upload file
        upload_response = requests.post(
            f"{self.base_url}/upload",
            headers=self.headers,
            data=read_file(file_path)
        )

        if upload_response.status_code != 200:
            raise RuntimeError(f"Upload failed: {upload_response.text}")

        return upload_response.json()["upload_url"]

    def analyze_audio(self, audio_path: str, is_url: bool = False) -> List[AudioSegment]:
        """
        Analyze audio content using AssemblyAI's API

        Args:
            audio_path (str): Path to audio file or URL
            is_url (bool): Whether the audio_path is a URL

        Returns:
            List[AudioSegment]: List of analyzed audio segments
        """
        # First verify the file exists
        if not is_url and not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Processing audio from: {audio_path}")

        # Handle file upload if needed
        try:
            audio_url = audio_path if is_url else self._upload_file(audio_path)
            print(f"Audio successfully uploaded. URL: {audio_url}")
        except Exception as e:
            raise RuntimeError(f"Failed to upload file: {str(e)}")

        # Create transcription request
        # Adjust payload to match AssemblyAI API schema
        data = {
            "audio_url": audio_url,
            "auto_highlights": True,  # Updated key for highlights
            "iab_categories": True,  # Enable topic detection
            "sentiment_analysis": True
        }

        # Start transcription
        print("Sending transcription request to AssemblyAI...")
        response = requests.post(
            f"{self.base_url}/transcript",
            headers=self.headers,
            json=data
        )

        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            raise RuntimeError(f"Failed to create transcription. Status code: {response.status_code}")

        try:
            transcript_id = response.json()["id"]
            print(f"Transcription started. ID: {transcript_id}")
        except KeyError:
            print(f"Unexpected API response: {response.text}")
            raise RuntimeError("Failed to get transcription ID from API response")

        # Poll for results
        polling_endpoint = f"{self.base_url}/transcript/{transcript_id}"

        print("\nProcessing audio... This may take a while.")
        print("Progress updates every 30 seconds:")

        while True:
            response = requests.get(polling_endpoint, headers=self.headers)
            transcript = response.json()

            status = transcript.get("status")
            print(f"\rStatus: {status}", end="", flush=True)

            if status == "completed":
                print("\nProcessing completed!")
                break
            elif status == "error":
                error = transcript.get("error", "Unknown error")
                raise RuntimeError(f"Transcription failed: {error}")
            else:
                time.sleep(30)  # Check every 30 seconds

        # Process results into segments
        segments = []
        chapters = transcript.get("chapters", [])

        if not chapters:
            print("Warning: No chapters found in the transcript")
            return segments

        for chapter in chapters:
            segment = AudioSegment(
                start_ms=chapter["start"],
                end_ms=chapter["end"],
                text=chapter.get("summary", ""),
                topics=chapter.get("topics", []),
                sentiment=chapter.get("sentiment", "neutral"),
                confidence=chapter.get("confidence", 1.0)
            )
            segments.append(segment)

        return segments

class ContentMatcher:
    def __init__(self):
        self.segments: List[AudioSegment] = []

    def add_segments(self, segments: List[AudioSegment]):
        """Add audio segments to the matcher"""
        self.segments.extend(segments)

    def match_content(self, user_preferences: Dict) -> List[Tuple[AudioSegment, float]]:
        """Match audio segments against user preferences"""
        matches = []

        for segment in self.segments:
            score = 0.0

            # Match topics
            common_topics = set(segment.topics) & set(user_preferences.get('topics', []))
            score += len(common_topics) * 0.5

            # Match sentiment
            if segment.sentiment == user_preferences.get('preferred_tone'):
                score += 0.3

            # Weight by confidence
            score *= segment.confidence

            if score > 0:
                matches.append((segment, score))

        return sorted(matches, key=lambda x: x[1], reverse=True)
