from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/<path:filename>')
def serve_file(filename):
    games_dir = os.path.join(os.getcwd(), "games")
    return send_from_directory(games_dir, filename)

if __name__ == "__main__":
    os.makedirs("games", exist_ok=True)
    app.run(host="0.0.0.0", port=8080)
