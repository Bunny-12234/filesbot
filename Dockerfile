FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install flask discord.py aiohttp

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python server.py & python main.py"]
