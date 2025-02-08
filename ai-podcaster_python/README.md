# AI Podcaster Python

AI-powered podcast script generation and audio synthesis tool.

## Project Structure

```
ai-podcaster_python/
├── json_script/         # JSON script templates and generation
│   ├── create/         # Script creation utilities
│   └── sample_script.json   # Sample script format
├── main.py             # Main application entry point
├── .env                # Environment variables (not tracked)
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Setup

1. Clone the repository
2. Create a `.env` file with required environment variables
3. Install dependencies
4. Run `main.py`

## Usage

1. Place your script template in `json_script/`
2. Run the main application
3. Generated audio files will be in `output/`

## Script Format

Scripts should follow this format:

```json
{
    "title": "Sample Title",
    "description": "Script description",
    "reference": "Reference source",
    "script": [
        {
            "text": "Narration text",
            "speaker": "Narrator",
            "speed": 1.0
        }
    ]
}
```