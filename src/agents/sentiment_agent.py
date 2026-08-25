class SentimentAgent:
    def analyze(self, text: str) -> str:
        negative = {"angry", "frustrated", "urgent", "terrible", "hate", "crash"}
        angry = {"angry", "useless", "garbage", "stupid", "incompetent", "idiots"}
        positive = {"thanks", "great", "happy", "appreciate"}
        words = set(text.lower().split())
        if words & angry:
            return "angry"
        if words & negative:
            return "negative"
        if words & positive:
            return "positive"
        return "neutral"
