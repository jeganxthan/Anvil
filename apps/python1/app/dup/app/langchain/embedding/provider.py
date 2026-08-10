from langchain_huggingface import HuggingFaceEmbeddings


class HuggingFaceEmbeddingProvider:


    def create(
        self,
        model_name: str,
        device: str = "cpu",
    ) -> HuggingFaceEmbeddings:

        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={
                "device": device,
            },
        )