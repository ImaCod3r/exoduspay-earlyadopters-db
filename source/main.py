from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from database import Email

app = Flask(__name__)
CORS(app)

@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/emails')
def saveEmail():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        new_email = Email.create(email=email)
        return jsonify({
            "message": "Email added successfully",
            "email": new_email.email,
            "time": new_email.formatted_time
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.get('/api/emails')
def getEmails():
    try:
        emails = Email.select()
        email_list = [{"email": e.email, "time": e.formatted_time} for e in emails]
        return jsonify(email_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.delete('/api/emails')
def deleteEmail():
    data = request.get_json()
    email = data.get("email")
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    try:
        deleted = Email.delete(email)
        if deleted:
            return jsonify({"message": "Email deleted successfully"}), 200
        else:
            return jsonify({"error": "Email not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get('/api/emails/stats')
def getStats():
    try:
        stats = Email.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)