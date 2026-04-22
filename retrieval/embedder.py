from typing import Dict, List

from retrieval.emb_model_loader import ModelLoader

"""
Embeds text into vectors using a pre-trained model.
Input: text
Output: vector
Uses components from the ingestion module.
Uses components from the embedding_model module.
"""


class Embedder:

    def __init__(self):
        self.model = ModelLoader.get_model()

    def embed_text(self, prepared_chunks: List[Dict[str, str]]):
        """
        embed_text takes a list of prepared chunks and returns a list of chunks with embeddings
        The embedding is added to the chunk as a new key-value pair.
        Each chunk is a dict with keys: chunk_id, chunk_text, metadata
        The metadata is a dict with keys: call_id, type, error_code, session_start_time, session_duration_sec, error_text

        :param prepared_chunks:
        :return:
        """
        print(
            "\n "
            + "\n Length of prepared_chunks :: "
            + str(len(prepared_chunks))
            + "\n"
        )

        text_to_embed = [item["chunk_text"] for item in prepared_chunks]

        print(":::Embedding Text:::")
        print(
            "\n "
            + "\n Length of text_to_embed :: "
            + str(len(text_to_embed))
            + "\n  Type:: "
            + str(type(text_to_embed))
            + "\n  "
        )
        embeddings = self.model.encode(text_to_embed)
        print(":::Embedding Complete:::")

        # map back
        for i, item in enumerate(prepared_chunks):
            item["embedding"] = embeddings[i].tolist()

        return prepared_chunks
