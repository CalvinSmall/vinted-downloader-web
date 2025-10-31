from flask import Flask, render_template, request, send_file, redirect
import subprocess
import os
import uuid
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    options = []
    if request.form.get('seller'):
        options.append('--seller')
    if request.form.get('all'):
        options.append('--all')
    if request.form.get('save_in_dir'):
        options.append('--save-in-dir')
    
    # Create unique directory for this download
    download_id = str(uuid.uuid4())
    download_path = os.path.join(UPLOAD_FOLDER, download_id)
    os.makedirs(download_path, exist_ok=True)
    
    # Run vinted-downloader
    try:
        cmd = ['vinted-downloader', *options, url, '-o', download_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Create zip archive
        zip_path = os.path.join(UPLOAD_FOLDER, f'{download_id}.zip')
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', download_path)
        
        return send_file(zip_path, as_attachment=True)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}", 500
    finally:
        # Cleanup
        shutil.rmtree(download_path, ignore_errors=True)
        if os.path.exists(zip_path):
            os.remove(zip_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)