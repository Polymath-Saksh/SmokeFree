from azure.communication.email import EmailClient
from django.conf import settings
import logging
import os
import dotenv  #Load environment variables from .env


logger = logging.getLogger(__name__)

def send_craving_notification(craving, recipients):
    """
    Send an email notification to all team members (except the logger)
    when a craving is logged, using Azure Communication Services.
    """
    sender_address = os.environ.get("AZURE_SENDER_ADDRESS")  # Always use settings for sender  # Always use settings for sender


    dotenv.load_dotenv()

    # Debug: Print sender and recipients
    logger.info(f"Azure Sender Address: {sender_address}")
    logger.info(f"Recipients: {recipients}")

    if not sender_address:
        logger.error("Azure sender address is not set in settings.")
        return False

    if not recipients:
        logger.warning("No recipients provided for craving notification.")
        return False

    try:
        client = EmailClient.from_connection_string(os.environ.get("AZURE_EMAIL_CONNECTION_STRING"))

        message = {
            "senderAddress": sender_address,
            "recipients": {
                "to": [{"address": email} for email in recipients]
            },
            "content": {
                "subject": f"New Craving Logged by {craving.user.username}",
                "plaintext": f"Your friend {craving.user.username} logged a craving with intensity {craving.intensity}/5. Check the team dashboard for more details.",
                "html": f"""
                    <html>
                        <body>
                            <h3>New Craving Alert 🚨</h3>
                            <p><strong>User:</strong> {craving.user.username}</p>
                            <p><strong>Intensity:</strong> {craving.intensity}/5</p>
                            <p><strong>Trigger:</strong> {craving.trigger or 'None'}</p>
                            <p><strong>Notes:</strong> {craving.notes or 'None'}</p>
                            <p><strong>Time:</strong> {craving.timestamp.strftime('%Y-%m-%d %H:%M')}</p>
                            <hr>
                            <p>View team progress: <a href="https://your-domain.com/teams/dashboard">Team Dashboard</a></p>
                        </body>
                    </html>
                """
            },
            
        }

        poller = client.begin_send(message)
        while not poller.done():
            poller.wait(5)  # Check every 5 seconds

        result = poller.result()
        if result["status"] == "Succeeded":
            logger.info("Craving notification email sent successfully.")
            return True
        else:
            logger.error(f"Email send failed with status: {result['status']}")
            return False

    except Exception as e:
        logger.error(f"Email send failed: {str(e)}", exc_info=True)
        return False