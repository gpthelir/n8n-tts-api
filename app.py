from flask import Flask, request, send_file
import edge_tts
import asyncio
import os

# Create the Flask app
app = Flask(__name__)

# Define the path for the output audio file
# On Render, /tmp is a temporary writable directory
OUTPUT_FILE = "/tmp/output.mp3"

@app.route('/tts', methods=['POST'])
async def tts_endpoint():
    if not request.is_json:
        return "Error: Request body must be JSON", 400
    data = request.get_json()
    if 'text' not in data:
        return "Error: 'text' field is missing from JSON body", 400

    text_to_speak = data['text']
    voice = data.get('voice', 'fa-IR-FaridNeural') # Using Farid's voice

    try:
        communicate = edge_tts.Communicate(text_to_speak, voice)
        await communicate.save(OUTPUT_FILE)
    except Exception as e:
        return f"Error generating speech: {str(e)}", 500

    if not os.path.exists(OUTPUT_FILE):
        return "Error: Could not create the audio file.", 500

    return send_file(OUTPUT_FILE, mimetype='audio/mpeg')
