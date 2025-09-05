FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 8080

# Run both Flask and Discord bot
CMD ["bash", "-c", "python server.py & python main.py"]
