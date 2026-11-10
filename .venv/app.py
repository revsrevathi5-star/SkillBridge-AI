
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "development-only-key"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "success",
        "message": "SkillBridge AI is running!"
    })


if __name__ == "__main__":
    app.run(debug=True)
