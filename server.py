from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)  # looks for ./templates and ./static by default

@app.route("/")
def index():
    # Renders templates/index.html provided by the starter
    return render_template("index.html")

# NOTE: The assignment requires this exact route name
@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyze:
        return "Invalid input! Please enter some text.", 400

    try:
        result = emotion_detector(text_to_analyze)
    except Exception as exc:
        # Keep response simple for the provided frontend
        return f"Error: {exc}", 502

    # Build the required sentence format
    anger   = result.get("anger", 0)
    disgust = result.get("disgust", 0)
    fear    = result.get("fear", 0)
    joy     = result.get("joy", 0)
    sadness = result.get("sadness", 0)
    dominant = result.get("dominant_emotion", "unknown")

    formatted = (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )
    return formatted, 200

if __name__ == "__main__":
    # Runs on localhost:5000 as required
    app.run(host="127.0.0.1", port=5000)
