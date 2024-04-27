from flask import Flask, request, send_file
import pyttsx3
import io
import os

app = Flask(__name__)

# Khởi tạo engine
engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

# Thiết lập các thuộc tính cho engine
engine.setProperty('rate', 140)    # Tốc độ đọc (từ 50 đến 200)
engine.setProperty('volume', 0.9)   # Âm lượng (từ 0 đến 1)

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')

    # Tạo một tệp tạm thời để lưu trữ âm thanh
    temp_file = "temp_audio.wav"
    
    # Chuyển đổi văn bản thành âm thanh và lưu vào tệp tạm thời
    engine.save_to_file(text, temp_file)
    engine.runAndWait()

    # Đọc dữ liệu từ tệp tạm thời và gửi lại như một phản hồi
    with open(temp_file, 'rb') as f:
        audio_data = f.read()

    # Xóa tệp tạm thời
    os.remove(temp_file)

    # Trả về file audio như một phản hồi
    return send_file(
        io.BytesIO(audio_data),
        mimetype='audio/mp3'
    )

if __name__ == '__main__':
    app.run(debug=True)