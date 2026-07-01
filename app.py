from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    resp = MessagingResponse()
    resp.message(f"You said: {incoming_msg}")
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
