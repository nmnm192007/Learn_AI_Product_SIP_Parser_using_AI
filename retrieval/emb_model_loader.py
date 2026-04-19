from sentence_transformers import SentenceTransformer


class ModelLoader:
    """
    Singleton class to load the embedding model
    only once and reuse it throughout the application.
    model_path = "all-MiniLM-L6-v2"
    or local path to the model
    """

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model
