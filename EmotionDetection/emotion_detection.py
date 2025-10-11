import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

# Reusable session with retries
_session = requests.Session()
_retries = Retry(total=3, backoff_factor=0.8, status_forcelist=(502, 503, 504), raise_on_status=False)
_adapter = HTTPAdapter(max_retries=_retries)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)

_EMPTY_RESULT = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None
}

def emotion_detector(text_to_analyze: str):
    """Return five emotions + dominant_emotion.
       If endpoint responds 400 (blank/invalid), return all None values."""
    payload = {"raw_document": {"text": text_to_analyze if text_to_analyze is not None else ""}}

    try:
        resp = _session.post(URL, headers=HEADERS, json=payload, timeout=20)
    except requests.exceptions.RequestException as e:
        # Network-level issue: surface a clear error
        raise ConnectionError(f"Network error: {e}") from e

    # --- Task 7 requirement: if server returns 400 for blank input, return None values ---
    if resp.status_code == 400:
        return _EMPTY_RESULT

    if resp.status_code != 200:
        # Any other non-OK status should be raised to the caller
        raise RuntimeError(f"Watson endpoint returned {resp.status_code}: {resp.text[:200]}")

    # Parse JSON and format like Task 3
    response_dict = json.loads(resp.text)
    emotions = response_dict.get("emotionPredictions", [{}])[0].get("emotion", {})

    anger   = emotions.get("anger", 0)
    disgust = emotions.get("disgust", 0)
    fear    = emotions.get("fear", 0)
    joy     = emotions.get("joy", 0)
    sadness = emotions.get("sadness", 0)

    scores = {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness
    }
    scores["dominant_emotion"] = max(scores, key=scores.get) if scores else None
    return scores
