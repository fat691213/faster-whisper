


FROM python:3.9-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 建立工作目錄
WORKDIR /audio

# 複製推論腳本（請確保 infer.py 存在）
#COPY infer.py .

# 安裝 Python 套件
RUN pip install --no-cache-dir \
    torch torchvision torchaudio faster-whisper \
    moviepy ffmpeg-python

# 預設執行指令
#CMD ["python3", "infer.py"]

