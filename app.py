from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Store appeals in memory (or you can hook up a database)
appeals = []

@app.route('/api/appeal', methods=['POST'])
def receive_appeal():
    data = request.json
    user_id = data.get("userId")
    appeal_text = data.get("appealText")

    if not user_id or not appeal_text:
        return jsonify({"error": "Missing userId or appealText"}), 400

    # Store appeal
    appeals.append({"userId": user_id, "appealText": appeal_text})

    return jsonify({"message": "Appeal submitted successfully"}), 200

@app.route('/admin')
def admin():
    # Simple admin page listing appeals
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
