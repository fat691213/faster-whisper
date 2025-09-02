

import os
import json
from faster_whisper import WhisperModel

# 使用 CPU 執行模型
model = WhisperModel("tiny", device="cpu")

# 音訊資料夾路徑
audio_dir = "/audio"
output_dir = "/audio/output"
os.makedirs(output_dir, exist_ok=True)

# 支援的音訊副檔名
supported_extensions = {".wav", ".mp3", ".flac", ".m4a", ".ogg", ".webm", ".aac", ".wma"}

# 批次處理音訊檔案
for filename in os.listdir(audio_dir):
    if any(filename.endswith(ext) for ext in supported_extensions):
        audio_path = os.path.join(audio_dir, filename)
        print(f"\n🔊 處理檔案: {filename}")

        segments, info = model.transcribe(audio_path, word_timestamps=True)

        # 建立輸出內容
        transcript_lines = [f"語言偵測: {info.language} (機率: {info.language_probability:.2f})"]
        transcript_json = {
            "file": filename,
            "language": info.language,
            "language_probability": info.language_probability,
            "segments": []
        }

        for segment in segments:
            line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
            transcript_lines.append(line)
            transcript_json["segments"].append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })

        # 儲存為 .txt
        txt_path = os.path.join(output_dir, filename + ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(transcript_lines))

        # 儲存為 .json
        json_path = os.path.join(output_dir, filename + ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(transcript_json, f, ensure_ascii=False, indent=2)

        print(f"✅ 已儲存: {txt_path} 和 {json_path}")

