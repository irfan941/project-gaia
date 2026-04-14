from functools import lru_cache
from fastembed import TextEmbedding


@lru_cache(maxsize=1)
def get_model() -> TextEmbedding:
    # Downloads ~130MB on first run, cached locally after that
    return TextEmbedding("BAAI/bge-small-en-v1.5")


def embed(text: str) -> list[float]:
    model = get_model()
    return next(model.embed([text])).tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return [e.tolist() for e in model.embed(texts)]
