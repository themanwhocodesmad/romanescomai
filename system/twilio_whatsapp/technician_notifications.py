import os
from twilio.rest import Client


def send_whatsapp_message(name, job_number, phone_number):
    TWILIO_ACCOUNT_SID = "AC02d73dbcb93cc95b9828f60caba7916b"
    TWILIO_AUTH_TOKEN = "dba6d118cf0937afd10d322b0540e719"

    print(f"SID: {TWILIO_ACCOUNT_SID}, Token: {TWILIO_AUTH_TOKEN}")  # Print the retrieved credentials

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    from_number = 'whatsapp:+14155238886'  # the Twilio phone number
    to_number = f'whatsapp:{phone_number}'
    body = f'Hello {name}, you have been assigned new job: *{job_number}*'
    message = client.messages.create(from_=from_number, body=body, to=to_number)
    return message
