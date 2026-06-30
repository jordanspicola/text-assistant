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

if __name__ == "__main__":
    app.run(debug=True, port=5000)

