import os
import uuid
import logging
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import your custom modules
from upload import upload_to_s3
from transcribe import transcribe_audio, get_transcript_content
from email_sender import send_email

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) # Needed for flashing messages
app.config['UPLOAD_FOLDER'] = 'transcriptions'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Get configuration from environment variables
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
if not S3_BUCKET:
    raise ValueError("S3_BUCKET_NAME environment variable not set.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. Get Form Data
    email = request.form.get('email')
    language = request.form.get('language')
    if 'file' not in request.files or not email or not language:
        flash('Missing form data. Please fill out all fields.')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file.')
        return redirect(url_for('index'))

    # 2. Save File Locally
    original_filename = secure_filename(file.filename)
    file_extension = os.path.splitext(original_filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create a user-specific directory
    user_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], email.replace('@', '_at_'))
    os.makedirs(user_upload_dir, exist_ok=True)
    local_file_path = os.path.join(user_upload_dir, unique_filename)
    
    try:
        file.save(local_file_path)
        logging.info(f"File saved locally at {local_file_path}")
    except Exception as e:
        logging.error(f"Failed to save file locally: {e}")
        return render_template('result.html', error="Could not save the uploaded file.")

    # 3. Upload to S3
    s3_object_key = f"transcriptions/{email}/{unique_filename}"
    if not upload_to_s3(local_file_path, S3_BUCKET, s3_object_key):
        return render_template('result.html', error="Failed to upload file to S3.")

    # 4. Transcribe Audio
    transcript_uri = transcribe_audio(S3_BUCKET, s3_object_key, language)
    if not transcript_uri:
        return render_template('result.html', error="Failed to start or complete the transcription job.")
        
    transcript_text = get_transcript_content(transcript_uri)
    if not transcript_text:
        return render_template('result.html', error="Could not retrieve the final transcript content.")

    # 5. Send Email
    email_subject = "Your Audio Transcription is Ready"
    email_body = f"Hello,\n\nHere is the transcription from your recently uploaded audio file:\n\n---\n{transcript_text}\n---\n\nThank you for using our service."
    send_email(email, email_subject, email_body)

    # 6. Clean up local file
    try:
        os.remove(local_file_path)
        logging.info(f"Cleaned up local file: {local_file_path}")
    except OSError as e:
        logging.error(f"Error removing local file {local_file_path}: {e}")

    # 7. Display Result
    return render_template('result.html', transcript=transcript_text, email=email)


if __name__ == '__main__':
    # Flask runs on port 5000 by default. To run on 8080:
    app.run(host='0.0.0.0', port=8080, debug=True)
