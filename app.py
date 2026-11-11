import os
import io
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "1513272617")

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/send_photo")
def send_photo():
    if not BOT_TOKEN:
        return jsonify(ok=False, error="Сервер ще не налаштований."), 500
    photo = request.files.get("photo")
    consent = request.form.get("consent")
    if consent != "yes" or not photo:
        return jsonify(ok=False, error="Потрібна згода та зроблене фото."), 400

    data = photo.read()
    if not data:
        return jsonify(ok=False, error="Файл порожній."), 400

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": "Фото надіслано зі сторінки NightShot за згодою користувача."},
            files={"photo": (photo.filename or "nightshot.jpg", io.BytesIO(data), photo.mimetype or "image/jpeg")},
            timeout=30,
        )
        result = response.json()
        if not response.ok or not result.get("ok"):
            return jsonify(ok=False, error="Telegram не прийняв фото. Перевірте налаштування бота."), 502
        return jsonify(ok=True)
    except requests.RequestException:
        return jsonify(ok=False, error="Не вдалося з'єднатися з Telegram."), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))