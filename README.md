# 2Embed Stream Resolver

A web application to resolve 2Embed stream URLs and extract direct video sources. Deployed on Render with a simple and elegant UI.

## Features

- 🎬 Resolve 2Embed URLs to direct video sources
- 🖼️ Extract iframe URLs
- 🎥 Detect m3u8 and mp4 stream URLs
- 📋 Copy URLs to clipboard with one click
- 🚀 Fully deployable on Render
- 💜 Beautiful gradient UI

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Run the application:
```bash
python resolver.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Deploy to Render

### Option 1: Using render.yaml (Recommended)

1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and configure the service

### Option 2: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `2embed-stream-resolver`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium && playwright install-deps`
   - **Start Command**: `gunicorn resolver:app`
   - **Python Version**: `3.11.0`
5. Add environment variable:
   - **Key**: `PLAYWRIGHT_BROWSERS_PATH`
   - **Value**: `/opt/render/project/.cache/ms-playwright`
6. Click "Create Web Service"

## Usage

1. Open the web application
2. Enter a 2Embed URL (e.g., `https://www.2embed.cc/embed/...`)
3. Click "Resolve Stream"
4. View the extracted video sources, iframe URLs, and stream URLs
5. Click "Copy" to copy any URL to your clipboard

## Technologies Used

- **Backend**: Flask (Python)
- **Browser Automation**: Playwright
- **Web Server**: Gunicorn
- **Deployment**: Render
- **Frontend**: HTML, CSS, JavaScript

## Project Structure

```
.
├── resolver.py           # Main Flask application
├── templates/
│   └── index.html       # Web UI
├── requirements.txt      # Python dependencies
├── render.yaml          # Render configuration
├── Procfile             # Process configuration
├── runtime.txt          # Python version specification
└── README.md            # This file
```

## API Endpoints

- `GET /` - Main web interface
- `POST /resolve` - Resolve stream URL (accepts JSON: `{"url": "..."}`)
- `GET /health` - Health check endpoint

## Notes

- The application uses Playwright with Chromium for browser automation
- Response times may vary depending on the target website's loading speed
- Some streams may be protected or require additional authentication

## License

MIT License