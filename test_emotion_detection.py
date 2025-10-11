import unittest
from EmotionDetection import emotion_detector

class TestEmotionDetection(unittest.TestCase):

    def _assert_emotion(self, text, expected):
        """Helper to assert dominant emotion for given text."""
        result = emotion_detector(text)
        # Basic shape checks (helps peer graders understand failures)
        self.assertIsInstance(result, dict, "Result should be a dict")
        self.assertIn("dominant_emotion", result, "Result missing 'dominant_emotion'")
        self.assertIn("anger", result)
        self.assertIn("disgust", result)
        self.assertIn("fear", result)
        self.assertIn("joy", result)
        self.assertIn("sadness", result)
        # Main assertion
        self.assertEqual(
            result["dominant_emotion"], expected,
            msg=f"\nText: {text}\nGot: {result}\nExpected dominant: {expected}"
        )

    def test_joy(self):
        self._assert_emotion("I am glad this happened", "joy")

    def test_anger(self):
        self._assert_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        self._assert_emotion("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        self._assert_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        self._assert_emotion("I am really afraid that this will happen", "fear")


if __name__ == "__main__":
    unittest.main(verbosity=2)
