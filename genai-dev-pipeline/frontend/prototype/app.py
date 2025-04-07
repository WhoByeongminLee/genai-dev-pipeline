# frontend/prototype/app.py

import os
import time
import requests
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

BACKEND_URL = "http://localhost:8000/v1/scene01/generate"

def generate_safe_filename(filename: str) -> str:
    # 확장자 분리
    name, ext = os.path.splitext(filename)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_name = secure_filename(name) or "file"
    return f"{timestamp}_{safe_name}{ext}"

@app.route("/prototype", methods=["GET", "POST"])
def prototype():
    if request.method == "POST":
        message_type = request.form.get("message_type")
        life_stage = request.form.get("life_stage")
        channels = request.form.getlist("channels")
        prompt = request.form.get("prompt")

        file_path = ""
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:
            filename = generate_safe_filename(uploaded_file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            uploaded_file.save(save_path)
            file_path = save_path

        payload = {
            "message_type": message_type,
            "life_stage": life_stage,
            "channels": channels,
            "prompt": prompt,
            "file_url": file_path or None,
            "session_id": "session-proto-001",
            "history": [
                {"user": "첫 요청 예시입니다", "ai": "AI 응답입니다."},
                {"user": "두 번째 요청", "ai": "두 번째 응답"},
                {"user": "세 번째 요청", "ai": "세 번째 응답"}
            ]
        }

        try:
            response = requests.post(BACKEND_URL, json=payload)
            result = response.json()
            print("응답 내용:", result)

            if "result" in result:
                return render_template("prototype.html", result=result["result"], used_prompt=result["used_prompt"])
            else:
                return render_template("prototype.html", error=f"API 응답 오류: {result}")
        except Exception as e:
            return render_template("prototype.html", error=str(e))

    return render_template("prototype.html")




if __name__ == "__main__":
    app.run(debug=True, port=5000)
