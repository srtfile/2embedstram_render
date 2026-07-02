from flask import Flask, render_template, request, jsonify
from playwright.sync_api import sync_playwright
import re
import os

app = Flask(__name__)

def resolve_2embed_stream(url):
    """
    Resolve 2embed stream URL to get the actual video source
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the URL
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for video element or iframe
            page.wait_for_timeout(3000)
            
            # Try to extract video source
            video_sources = []
            
            # Method 1: Check for video tags
            videos = page.query_selector_all('video')
            for video in videos:
                src = video.get_attribute('src')
                if src:
                    video_sources.append(src)
            
            # Method 2: Check for iframes
            iframes = page.query_selector_all('iframe')
            iframe_urls = []
            for iframe in iframes:
                src = iframe.get_attribute('src')
                if src:
                    iframe_urls.append(src)
            
            # Method 3: Intercept network requests for m3u8/mp4
            streams = []
            page.on('response', lambda response: streams.append(response.url) 
                    if any(ext in response.url for ext in ['.m3u8', '.mp4']) else None)
            
            page.wait_for_timeout(2000)
            
            browser.close()
            
            return {
                'success': True,
                'video_sources': video_sources,
                'iframe_urls': iframe_urls,
                'streams': streams,
                'page_url': url
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/resolve', methods=['POST'])
def resolve():
    """API endpoint to resolve stream URLs"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
    
    result = resolve_2embed_stream(url)
    return jsonify(result)

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
