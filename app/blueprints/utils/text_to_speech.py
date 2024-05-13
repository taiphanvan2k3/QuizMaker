from flask import g
from .helpers import create_folder_if_not_exists
from datetime import datetime
from .firestore_utils import upload_file_to_fire_storage, initialize_firestore
import pyttsx3, os

current_dir = os.path.dirname(os.path.realpath(__file__))

# Khởi tạo engine
db = initialize_firestore()

engine = pyttsx3.init()
engine.setProperty(
    "voice",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
)

# Thiết lập các thuộc tính cho engine
engine.setProperty("rate", 140)  # Tốc độ đọc (từ 50 đến 200)
engine.setProperty("volume", 0.9)  # Âm lượng (từ 0 đến 1)


def text_to_speech(text: str):
    # Tạo một tệp tạm thời để lưu trữ âm thanh
    create_folder_if_not_exists("audios")
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y%m%d%H%M%S")

    current_user = g.user
    temp_file = f"{current_dir}/audios/{current_user.id}_{formatted_time}.mp3"

    # Chuyển đổi văn bản thành âm thanh và lưu vào tệp tạm thời
    engine.save_to_file(text, temp_file)
    engine.runAndWait()

    # Tải tệp tạm thời lên Firebase Storage
    public_url = upload_file_to_fire_storage(
        temp_file, file_name=f"{formatted_time}_{text}.mp3"
    )

    # Xóa tệp tạm thời
    os.remove(temp_file)

    # Tạo record lưu audio của từ vựng đó
    db.collection("audios").add(
        {
            "english": text,
            "audio_url": public_url,
        }
    )

    return public_url
