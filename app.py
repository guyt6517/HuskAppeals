from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Put your Discord webhook URL here or set it as environment variable DISCORD_WEBHOOK_URL
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

@app.route("/appeal", methods=["POST"])
def appeal():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400
    
    username = data.get("username", "").strip()
    userid = data.get("userid", "").strip()
    reason = data.get("reason", "").strip()
    
    if not username or not userid or not reason:
        return jsonify({"error": "Missing fields: username, userid, and reason are required."}), 400
    
    # Create Discord message payload
    content = (
        f"**New HuskAPI Appeal Submission**\n"
        f"**Username:** {username}\n"
        f"**UserID:** {userid}\n"
        f"**Reason:** {reason}"
    )
    
    discord_data = {
        "content": content
    }
    
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=discord_data)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": "Failed to send to Discord webhook", "details": str(e)}), 500
    
    return jsonify({"success": True, "message": "Appeal submitted successfully."}), 200


if __name__ == "__main__":
    app.run(debug=True)
