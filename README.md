
# AWS S3 Transcription Service with Flask

This is a web application built with Python and Flask that allows users to upload an audio file, transcribe it using the Amazon Transcribe service, and receive the full transcription via email and on-screen.

## Features

-   Simple web interface for uploading files.
-   Support for multiple languages for transcription.
-   Securely uploads files to a private Amazon S3 bucket.
-   Initiates and monitors an asynchronous transcription job on AWS.
-   Displays the final transcription result on a web page.
-   Sends the full transcript to the user's provided email address using SMTP.
-   Manages all credentials and sensitive information using environment variables.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Python 3.7+** and **pip**: [Download Python](https://www.python.org/downloads/)
2.  **An AWS Account**: You will need access to S3 and Transcribe services.
3.  **An S3 Bucket**: Create a new S3 bucket in your desired AWS region.
4.  **An IAM User**: Create an IAM user with programmatic access. Attach policies that grant permissions for S3 and Transcribe. For ease of setup, you can use `AmazonS3FullAccess` and `AmazonTranscribeFullAccess`, but for production, it's recommended to create a more restrictive custom policy. Note down the **Access Key ID** and **Secret Access Key**.
5.  **An SMTP Server**: The application is configured to use Zoho's SMTP server, but any standard SMTP server will work. You will need the host, port, username, and password for your email account.

## Local Installation and Setup

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository

First, clone the project repository to your local machine.

```bash
git clone <your-repository-url>
cd your-transcription-project
```

### 2. Create a Python Virtual Environment

It is highly recommended to use a virtual environment to isolate project dependencies.

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Create the Local Uploads Folder

The application needs a temporary directory to store files before they are uploaded to S3.

```bash
mkdir transcriptions
```

### 5. Configure Environment Variables

The application uses a `.env` file to manage all secrets and configuration settings. Create a file named `.env` in the root of the project directory.

Copy the following content into your new `.env` file and **fill in the values** with your own credentials.

```ini
# AWS Credentials
# Get these from your IAM User in the AWS Console
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
AWS_REGION=us-east-1  # The region your S3 bucket is in

# S3 Configuration
# The name of the S3 bucket you created
S3_BUCKET_NAME=your-s3-bucket-name

# SMTP Credentials for Sending Email
# Update these with your email provider's details
SMTP_HOST=smtp.zoho.com
SMTP_PORT=465
SMTP_USER=your-email@example.com
SMTP_PASS=your-email-password-or-app-password
```

**IMPORTANT:** Do NOT commit the `.env` file to version control. The included `.gitignore` file should already prevent this.

## Running the Application

Once the setup and configuration are complete, you can run the Flask web server.

```bash
python app.py
```

The application will start on port 8080 by default. You should see output similar to this:

```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:8080
Press CTRL+C to quit
```

Open your web browser and navigate to **[http://localhost:8080](http://localhost:8080)**.

## Usage Workflow

1.  Open the application in your browser.
2.  Enter your email address where you want to receive the transcript.
3.  Select the language spoken in the audio file.
4.  Choose the audio file you wish to transcribe (e.g., `.mp3`, `.wav`, `.mp4`).
5.  Click the "Transcribe" button.
6.  The application will process the file. This may take some time depending on the length of the audio.
7.  Once complete, a result page will display the full transcript.
8.  Simultaneously, an email containing the same transcript will be sent to the address you provided.

## Project Structure

```
/your-transcription-project/
├── .env                  # (You create this) Stores secret credentials
├── .gitignore            # Specifies files to ignore for Git
├── app.py                # Main Flask application logic
├── email_sender.py       # Module for sending emails via SMTP
├── requirements.txt      # List of Python dependencies
├── transcribe.py         # Module for interacting with AWS Transcribe
├── upload.py             # Module for uploading files to S3
|
├── templates/
│   ├── index.html        # The main upload form page
│   └── result.html       # The page to display the transcription result
|
└── transcriptions/       # (You create this) Temporary local storage for uploads
