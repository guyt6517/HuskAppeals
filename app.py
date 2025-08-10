from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# In-memory appeals storage for admin viewing (optional)
appeals = []

@app.route('/api/appeal', methods=['POST'])
def receive_appeal():
    data = request.json
    user_id = data.get("userId")
    appeal_text = data.get("appealText")

    if not user_id or not appeal_text:
        return jsonify({"error": "Missing userId or appealText"}), 400

    # Send to Discord webhook
    content = f"**New Appeal Received**\nUser ID: {user_id}\nAppeal:\n{appeal_text}"
    discord_data = {"content": content}
    r = requests.post(DISCORD_WEBHOOK_URL, json=discord_data)

    if r.status_code != 204:
        return jsonify({"error": "Failed to send to Discord"}), 500

    # Store appeal in memory (optional)
    appeals.append({"userId": user_id, "appealText": appeal_text})

    return jsonify({"message": "Appeal submitted successfully"}), 200

@app.route('/admin')
def admin():
    # Very basic admin page showing appeals in memory
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Admin Appeals</title></head>
    <body>
    <h1>Appeals Received</h1>
    {% for appeal in appeals %}
      <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
        <strong>User ID:</strong> {{ appeal.userId }}<br>
        <strong>Appeal:</strong><pre>{{ appeal.appealText }}</pre>
      </div>
    {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, appeals=appeals)

if __name__ == '__main__':
    app.run(debug=True)
