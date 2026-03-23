from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from PIL import Image, ImageChops, ImageEnhance
import hashlib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'data', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

# --- ELA Forgery Detection ---
def perform_ela(path, quality=90):
    original = Image.open(path).convert('RGB')
    temp_filename = os.path.join(UPLOAD_DIR, 'temp_ela.jpg')
    original.save(temp_filename, 'JPEG', quality=quality)
    temporary = Image.open(temp_filename)
    diff = ImageChops.difference(original, temporary)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff if max_diff != 0 else 1
    diff = ImageEnhance.Brightness(diff).enhance(scale)
    suspicious = max_diff > 30  # Lower threshold = more sensitive
    os.remove(temp_filename)
    return suspicious

def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = f.filename
    safe_name = filename.replace('..', '')
    dest_path = os.path.join(UPLOAD_DIR, safe_name)
    f.save(dest_path)

    sha = compute_sha256(dest_path)
    size = os.path.getsize(dest_path)
    mime = f.mimetype if hasattr(f, 'mimetype') else None
    upload_time = datetime.utcnow().isoformat()

    verdict = 'unknown'
    reason = ''
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        suspicious = perform_ela(dest_path)
        if suspicious:
            verdict = 'fake'
            reason = 'Image shows signs of editing (ELA)'
        else:
            verdict = 'original'
    # You can add similar logic for PDFs, DOCX, etc.
    return jsonify({'status': verdict, 'reason': reason, 'sha256': sha, 'size': size, 'mime': mime, 'upload_time': upload_time})

if __name__ == '__main__':
    app.run(port=5050)
