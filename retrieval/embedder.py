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

        :param prepared_chunks:List[Dict[str,str]]
        :return: prepared_chunks: List[Dict[str, str]]
        """

        if not prepared_chunks:
            return []

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
        print("Embeddings :: " + str(embeddings.shape))
        print(":::Embedding Complete:::")

        # map back
        for i, prep_chunk_item in enumerate(prepared_chunks):
            # Add the embedding to the chunk
            # prep_chunk_item holds the current prepared_chunks item and
            # we are adding an additional key:value with embedding:embeddings[i]
            # with i corresponding to
            # mapping index between prepared_chunks and embedding vectors

            prep_chunk_item["embedding"] = embeddings[i].tolist()

            print("Embedding index Added to Chunk :: " + str(i))
            print("Chunk ID :: " + str(prep_chunk_item["chunk_id"]))
            print("Length of Embedding :: " + str(len(prep_chunk_item["embedding"])))

        print(len(prepared_chunks[0]["embedding"]))

        return prepared_chunks


#
# Result of the test run
#
# \AppData\Local\Programs\Python\Python314\python.exe "\Phase0\Learn_AI_Product_Answering_Machine_using_AI\run.py"
# Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
# Loading weights: 100%|██████████| 103/103 [00:00<00:00, 2300.06it/s]
# BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2
# Key                     | Status     |  |
# ------------------------+------------+--+-
# embeddings.position_ids | UNEXPECTED |  |
#
# Notes:
# - UNEXPECTED:	can be ignored when loading from different task/architecture; not ok if you expect identical arch.
# Model ID: 1850459002192
#
#
#  Length of prepared_chunks :: 13
#
# :::Embedding Text:::
#
#
#  Length of text_to_embed :: 13
#   Type:: <class 'list'>
#   embeddings :: (13, 384)
# :::Embedding Complete:::
# Embedding Added to Chunk :: 0
# Chunk ID :: 1-1415@192.4.36.31_1
# Length of Embedding :: 384
# Embedding Added to Chunk :: 1
# Chunk ID :: 1-1415@192.4.36.31_2
# Length of Embedding :: 384
# Embedding Added to Chunk :: 2
# Chunk ID :: 1-1415@192.4.36.31_3
# Length of Embedding :: 384
# Embedding Added to Chunk :: 3
# Chunk ID :: 1-1415@192.4.36.31_4
# Length of Embedding :: 384
# Embedding Added to Chunk :: 4
# Chunk ID :: 1-1415@192.4.36.31_5
# Length of Embedding :: 384
# Embedding Added to Chunk :: 5
# Chunk ID :: 2dtiptxwgkup@testsv15_1
# Length of Embedding :: 384
# Embedding Added to Chunk :: 6
# Chunk ID :: 2dtiptxwgkup@testsv15_2
# Length of Embedding :: 384
# Embedding Added to Chunk :: 7
# Chunk ID :: 2dtiptxwgkup@testsv15_3
# Length of Embedding :: 384
# Embedding Added to Chunk :: 8
# Chunk ID :: 2dtiptxwgkup@testsv15_4
# Length of Embedding :: 384
# Embedding Added to Chunk :: 9
# Chunk ID :: 1507jrp93xkl0@testsv15_1
# Length of Embedding :: 384
# Embedding Added to Chunk :: 10
# Chunk ID :: 1507jrp93xkl0@testsv15_2
# Length of Embedding :: 384
# Embedding Added to Chunk :: 11
# Chunk ID :: 133wk5zi500yl@testsv15_1
# Length of Embedding :: 384
# Embedding Added to Chunk :: 12
# Chunk ID :: 133wk5zi500yl@testsv15_2
# Length of Embedding :: 384
# 384
#
# Process finished with exit code 0
#
#
#
