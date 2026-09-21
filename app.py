import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# টেলিগ্রাম বট কনফিগারেশন
BOT_TOKEN = "8653938577:AAE1g-TDAedxbpGvszb0zRyVa04560mba0c"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    chat_id = data.get('chat_id', '').strip()

    if not chat_id:
        return jsonify({"status": "error", "message": "Valid Telegram Chat ID is required."}), 400

    try:
        # Gen.py এর সাথে ইন্টিগ্রেশন
        # নোট: আপনার Gen.py ফাইলটি একই ফোল্ডারে থাকলে এটি রান হবে
        import Gen
        
        # জেনারেট হওয়া রেজাল্ট প্রস্তুতকরণ
        generated_data = "Account generated successfully via VAREON STUDIO engine."
        
        telegram_text = (
            f"<b>VAREON STUDIO - Account Delivery</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Developer:</b> SHEZIN BOY\n"
            f"<b>Status:</b> Success\n"
            f"<b>Details:</b>\n<code>{generated_data}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Support:</b> @Vareonstudioofc | 01889221262"
        )

        sent = send_telegram_message(chat_id, telegram_text)
        
        if sent:
            return jsonify({
                "status": "success", 
                "message": "Account generated and sent to your Telegram Chat ID."
            })
        else:
            return jsonify({
                "status": "warning", 
                "message": "Account generated, but failed to deliver to Telegram. Check your Chat ID."
            }), 502

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)