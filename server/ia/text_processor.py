import re
import unicodedata
from collections import Counter


# Lista própria, conforme solicitado no trabalho.
STOPWORDS_PT = {
    "a", "ao", "aos", "as", "à", "às", "aquele", "aquela", "aqueles", "aquelas",
    "aquilo", "até", "com", "como", "contra", "da", "das", "de", "dela", "delas",
    "dele", "deles", "depois", "do", "dos", "e", "é", "em", "entre", "era", "eram",
    "essa", "essas", "esse", "esses", "esta", "estas", "este", "estes", "eu", "foi",
    "foram", "há", "isso", "isto", "já", "lhe", "lhes", "mais", "mas", "me", "mesmo",
    "na", "nas", "nem", "no", "nos", "nós", "num", "numa", "o", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "qual", "quando", "que", "quem", "se",
    "sem", "ser", "seu", "seus", "sua", "suas", "são", "também", "te", "tem", "tendo",
    "ter", "tinha", "tinham", "tu", "um", "uma", "umas", "uns", "vai", "vão", "vos",
}


class TextProcessor:
    """Normaliza o livro, tokeniza, remove stopwords e cria o vocabulário."""

    def __init__(self, min_frequency=2):
        self.min_frequency = min_frequency

    @staticmethod
    def normalize(text):
        text = text.lower()
        text = unicodedata.normalize("NFD", text)
        text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def tokenize(self, text):
        normalized = self.normalize(text)
        return normalized.split()

    def process(self, text):
        tokens = self.tokenize(text)
        tokens = [t for t in tokens if t not in STOPWORDS_PT and len(t) > 2]
        frequencies = Counter(tokens)
        vocabulary = sorted(
            word for word, count in frequencies.items()
            if count >= self.min_frequency
        )
        return {
            "tokens": tokens,
            "frequencias": frequencies,
            "vocabulario": vocabulary,
        }
