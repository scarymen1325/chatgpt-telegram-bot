FROM python:3.9-alpine

ENV PYTHONFAULTHANDLER=1 \
     PYTHONUNBUFFERED=1 \
     PYTHONDONTWRITEBYTECODE=1 \
     PIP_DISABLE_PIP_VERSION_CHECK=on

RUN if [ -f "/etc/alpine-release" ]; then \
        apk --no-cache add ffmpeg gcc musl-dev python3-dev; \
    elif [ -f "/etc/lsb-release" ]; then \
        apt-get update && \
        apt-get install -y ffmpeg gcc python3-dev libffi-dev && \
        rm -rf /var/lib/apt/lists/*; \
    else \
        echo "Unsupported OS" && exit 1; \
    fi

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "bot/main.py"]