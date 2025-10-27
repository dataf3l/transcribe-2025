import smtplib
import ssl
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email(destination, subject, message):
    """
    Sends an email using Zoho SMTP credentials from environment variables.
    """
    host = os.getenv('SMTP_HOST')
    port = int(os.getenv('SMTP_PORT', 465))
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASS')

    if not all([host, port, user, password]):
        logging.error("SMTP environment variables not set. Cannot send email.")
        return False

    context = ssl.create_default_context()
    
    email_message = f"Subject: {subject}\n\n{message}"

    try:
        logging.info(f"Connecting to SMTP server to send email to {destination}...")
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(user, password)
            server.sendmail(user, destination, email_message.encode('utf-8'))
            logging.info("Email sent successfully.")
            return True
    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP Authentication Error. Check your SMTP_USER and SMTP_PASS.")
        return False
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False
