from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'frontend/prototype/uploads'

BACKEND_URL = "http://localhost:8000/v1/scene01/generate"

@app.route("/prototype", methods=["GET", "POST"])
def prototype():
    if request.method == "POST":
        message_type = request.form.get("message_type")
        life_stage = request.form.get("life_stage")
        channels = request.form.getlist("channels")
        prompt = request.form.get("prompt")

        # 파일 업로드 처리
        uploaded_file = request.files.get("file")
        file_path = ""
        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(save_path)
            file_path = save_path  # 임시로 로컬 경로 사용

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
