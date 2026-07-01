import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="You are a helpful personal assistant. Keep replies concise since they are delivered via SMS.",
        messages=[{"role": "user", "content": incoming_msg}]
    )
    
    reply = message.content[0].text
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

@app.route("/")
def home():
    return "Text assistant is running."

@app.route("/privacy")
def privacy():
    return "This application is a personal assistant tool used solely by its owner. Phone numbers and message content are used only to provide the requested service and are not shared, sold, or disclosed to any third party."

@app.route("/terms")
def terms():
    return "Personal Assistant SMS Service. This is a personal, single-user application. Message and data rates may apply. Message frequency varies. Reply HELP for help. Reply STOP to opt out at any time."

if __name__ == "__main__":
    app.run(debug=True, port=5000)
