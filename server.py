from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Required by the assignment
@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    text_to_analyze = request.args.get("textToAnalyze", "")

    try:
        result = emotion_detector(text_to_analyze)
    except Exception as exc:
        return f"Error: {exc}", 502

    # Handle blank/invalid input per Task 7
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!", 400

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
    app.run(host="127.0.0.1", port=5000)
