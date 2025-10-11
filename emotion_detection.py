import requests
import json

def emotion_detector(text_to_analyze):
    """
    Sends text to IBM Watson NLP EmotionPredict endpoint
    and returns the text part of the JSON response.
    """
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, headers=headers, json=payload)

    # If request fails, raise an error
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    # Return the textual JSON response
    return response.text
