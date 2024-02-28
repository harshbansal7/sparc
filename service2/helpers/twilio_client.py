from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

sid = os.getenv("TWILIO_ACCOUNT_SID")
auth = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(sid, auth)

def dispatch_message_to_whatsapp(packet):
    message = twilio_client.messages.create(
        from_='whatsapp:+14155238886',
        body=packet[0],
        to=f"whatsapp:{packet[1]}"
    )

    if not message.error_code:
        return True
    
    return False