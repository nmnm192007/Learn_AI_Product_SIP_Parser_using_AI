from emb_model_loader import ModelLoader


class Embedder:

    def __init__(self):
        self.model = ModelLoader.get_model()
