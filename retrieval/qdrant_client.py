from qdrant_client.models import Distance, PointStruct, VectorParams

from qdrant_client import QdrantClient


class QdrantVectorDB:

    def __init__(self):
        self.client = QdrantClient(":memory:")

    def store_embeddings(self, emb_chunks):
        collection_existing = self.client.get_collections().collections
        existing_col = [col.name for col in collection_existing]
        if "calls" not in existing_col:
            self.client.create_collection(
                collection_name="calls",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

        vector_points = []

        for idx, item in enumerate(emb_chunks):
            #     Use PointStruct to store the data in qdrant DB
            point = PointStruct(
                id=idx,
                vector=item["embedding"],
                payload={
                    "chunk_id": item["chunk_id"],
                    "chunk_text": item["chunk_text"],
                    "metadata": item["metadata"],
                },
            )
            vector_points.append(point)
        print(type(vector_points[0]))
        print(self.client.count("calls"))
        print(self.client.scroll("calls", limit=1))

        self.client.upsert(collection_name="calls", points=vector_points)

        print("After Insert Count:", self.client.count("calls"))
        record = self.client.scroll(collection_name="calls", limit=1, with_vectors=True)

        vec = record[0][0].vector

        print(len(vec))
        # print(
        #     "Sample Data:",
        #     self.client.scroll("calls", limit=1, with_vectors=True, with_payload=True),
        # )
