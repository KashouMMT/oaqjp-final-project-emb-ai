"""
EmotionDetection package

Exposes:
    emotion_detector(text: str) -> dict
"""

from .emotion_detection import emotion_detector

__all__ = ["emotion_detector"]
__version__ = "0.1.0"
