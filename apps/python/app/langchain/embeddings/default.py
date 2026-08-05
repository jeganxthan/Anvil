from langchain_huggingface import HuggingFaceEmbeddings

from app.langchain.embeddings.config import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_DEVICE,
    DEFAULT_MODEL,
    DEFAULT_NORMALIZE,
)
from app.langchain.embeddings.models import EmbeddingConfig

class DefaultEmbeddings(HuggingFaceEmbeddings):
    def __init__(self, config:EmbeddingConfig|None=None):
        config = config or EmbeddingConfig(
            model=DEFAULT_MODEL,
            device=DEFAULT_DEVICE,
            normalize=DEFAULT_NORMALIZE,
            batch_size=DEFAULT_BATCH_SIZE,
        )
        
        model_kwargs = {
            "device":config.device,
            **config.model_kwargs
        }
        
        encode_kwargs={
            "normalize_embeddings":config.normalize,
            "batch_size":config.batch_size,
            **config.encode_kwargs
        }
        
        super().__init__(
            model_name=config.model,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,        
        )