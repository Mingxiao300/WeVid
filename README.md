# SundAI - Podcast Analyzer

A Python application that analyzes YouTube videos/podcasts and provides personalized content recommendations based on user preferences.

## Features

- **Download & Process**: Automatically downloads YouTube videos and extracts audio
- **AI Analysis**: Uses AssemblyAI to transcribe, detect topics, and analyze sentiment
- **Smart Matching**: Matches content based on topics and sentiment preferences
- **Time-stamped Recommendations**: Get exact timestamps for segments you'll enjoy

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- AssemblyAI API key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd SundAI2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root:
```
ASSEMBLYAI_API_KEY=your_api_key_here
```

4. (Optional) For restricted videos, export cookies from your browser:
- Install a browser extension like "cookies.txt"
- Export cookies to `cookies.txt` in the project root

## Usage

Run the application:
```bash
python main.py
```

### Example Workflow

1. Enter a YouTube URL when prompted
2. Wait for the video to download and analyze
3. Enter your preferred topics (comma-separated):
   ```
   Technology, AI, Python
   ```
4. Enter your preferred tone:
   ```
   positive
   ```
5. Receive personalized recommendations with timestamps!

## Project Structure

```
SundAI2/
├── main.py                  # Main application entry point
├── audio_analyzer.py        # AssemblyAI integration and content matching
├── youtube_processor.py     # YouTube download and processing
├── requirements.txt         # Python dependencies
├── cookies.txt              # Browser cookies for restricted videos
├── downloads/               # Downloaded audio files
└── README.md               # This file
```

## Key Components

### AudioAnalyzer (`audio_analyzer.py`)
- Handles audio upload to AssemblyAI
- Performs transcription with auto-highlights
- Detects IAB categories (topics)
- Analyzes sentiment (positive/negative/neutral)
- Returns segmented audio data with metadata

### ContentMatcher (`audio_analyzer.py`)
- Scores segments based on user preferences
- Considers topic overlap and sentiment matching
- Returns ranked recommendations

### YouTubeProcessor (`youtube_processor.py`)
- Downloads YouTube videos using yt-dlp
- Extracts audio to MP3 format
- Handles progress tracking

## API Configuration

This project uses [AssemblyAI](https://www.assemblyai.com/) for audio transcription and analysis. 

**Get your API key:**
1. Sign up at https://www.assemblyai.com/
2. Copy your API key from the dashboard
3. Add it to your `.env` file

## Dependencies

- `requests` - HTTP library for API calls
- `python-dotenv` - Environment variable management
- `yt-dlp` - YouTube video downloader
- `ffmpeg` - Audio processing (system dependency)

## Future Enhancements

- Cache analyzed segments to avoid re-processing
- Support for batch processing multiple videos
- Export recommendations to different formats
- CLI arguments for automation
- Web interface

## Troubleshooting

**ImportError or ModuleNotFoundError**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**AssemblyAI API errors**
- Verify your API key is correct in `.env`
- Check your API quota and billing status

**Download errors**
- Ensure FFmpeg is installed and accessible
- For restricted videos, provide a valid `cookies.txt` file

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- AssemblyAI for transcription and audio analysis
- yt-dlp for YouTube downloading capabilities

