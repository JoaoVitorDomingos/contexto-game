from pathlib import Path
import requests


BOOK_URLS = [
    "https://www.gutenberg.org/cache/epub/26110/pg26110.txt",
    "https://www.gutenberg.org/files/26110/26110-8.txt",
]


class BookLoader:
    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir or Path(__file__).resolve().parent.parent / "data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.book_path = self.data_dir / "o_olho_de_vidro.txt"

    def load(self):
        if self.book_path.exists() and self.book_path.stat().st_size > 1000:
            return self.book_path.read_text(encoding="utf-8", errors="ignore")

        last_error = None
        for url in BOOK_URLS:
            try:
                response = requests.get(url, timeout=20)
                response.raise_for_status()
                text = response.content.decode("utf-8", errors="ignore")
                if len(text) > 1000:
                    self.book_path.write_text(text, encoding="utf-8")
                    return text
            except Exception as exc:
                last_error = exc

        raise RuntimeError(
            "Não foi possível carregar O Olho de Vidro. "
            "Coloque o arquivo de texto em server/data/o_olho_de_vidro.txt "
            "ou verifique sua conexão com a internet."
        ) from last_error
