from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

sid = os.getenv("TWILIO_ACCOUNT_SID")
auth = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(sid, auth)

def dispatch_message_to_whatsapp(msg, contactno):
    message = twilio_client.messages.create(
        from_='whatsapp:+14155238886',
        body=msg,
        to=f"whatsapp:{contactno}"
    )

    if not message.error_code:
        return str(message.sid)
    
    return False