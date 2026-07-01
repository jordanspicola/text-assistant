import os
import sqlite3
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def get_db():
    db = sqlite3.connect("conversations.db")
    db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    return db

def get_history(phone, limit=10):
    db = get_db()
    rows = db.execute(
        "SELECT role, content FROM messages WHERE phone = ? ORDER BY timestamp DESC LIMIT ?",
        (phone, limit)
    ).fetchall()
    db.close()
    rows.reverse()
    return [{"role": row[0], "content": row[1]} for row in rows]

def save_message(phone, role, content):
    db = get_db()
    db.execute(
        "INSERT INTO messages (phone, role, content) VALUES (?, ?, ?)",
        (phone, role, content)
    )
    db.commit()
    db.close()

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    phone = request.form.get("From", "")

    save_message(phone, "user", incoming_msg)
    history = get_history(phone)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="You are Jordan's personal AI assistant. Keep replies concise since they are delivered via SMS. You remember previous messages in the conversation.",
        messages=history
    )

    reply = message.content[0].text
    save_message(phone, "assistant", reply)

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
