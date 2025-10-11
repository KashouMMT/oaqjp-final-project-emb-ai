import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

_session = requests.Session()
_retries = Retry(total=3, backoff_factor=0.8, status_forcelist=(502, 503, 504))
_adapter = HTTPAdapter(max_retries=_retries)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)

def emotion_detector(text_to_analyze: str):
    if not text_to_analyze or not text_to_analyze.strip():
        raise ValueError("text_to_analyze must be a non-empty string.")

    payload = {"raw_document": {"text": text_to_analyze}}
    resp = _session.post(URL, headers=HEADERS, json=payload, timeout=20)

    if resp.status_code != 200:
        raise RuntimeError(f"Watson endpoint returned {resp.status_code}: {resp.text[:200]}")

    # --- Task 3: parse and format output ---
    response_dict = json.loads(resp.text)

    # navigate to the emotions section in the returned JSON
    emotions = response_dict.get("emotionPredictions", [{}])[0].get("emotion", {})

    anger = emotions.get("anger", 0)
    disgust = emotions.get("disgust", 0)
    fear = emotions.get("fear", 0)
    joy = emotions.get("joy", 0)
    sadness = emotions.get("sadness", 0)

    scores = {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness
    }

    # compute dominant emotion
    dominant = max(scores, key=scores.get)
    scores["dominant_emotion"] = dominant

    return scores
