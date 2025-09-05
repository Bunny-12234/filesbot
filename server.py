from flask import Flask, send_from_directory
import os

app = Flask(__name__)
GAMES_FOLDER = "games"  # folder where files will be stored

@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory(GAMES_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
