from qdrant_client.models import FieldCondition, Filter, MatchValue
from retrieval.emb_model_loader import ModelLoader
from retrieval.qdrant_client import QdrantVectorDB


class Retriever:
    def __init__(self, db):
        self._model = ModelLoader.get_model()
        self._client = db

    def check_collections(self, c_obj):
        collection_existing = self._client.client.get_collections().collections
        existing_col = [col.name for col in collection_existing]
        print(existing_col)

        if c_obj not in existing_col:
            print("Collections Not Found ::" + str(c_obj))
            raise ValueError(f"Collection {c_obj} not found in qdrant")
        return True

    def get_query_vector(self, query: str):
        query_vector = self._model.encode(query)
        print("Query Vector Shape :: " + str(query_vector.shape))
        print("Query Vector Length :: " + str(len(query_vector)))
        return query_vector

    def start_search(self, query: str):

        if not self.check_collections("calls"):
            raise ValueError("Collections object not found")
        # Check for the points stored
        # points = self._client.client.scroll(collection_name="calls", limit=3)
        #
        # for p in points[0]:
        #     print("Payload.p  ::   ")
        #     print(p.payload)
        # count = self._client.client.count(collection_name="calls")
        # print(count)
        search_result = self._client.client.query_points(
            collection_name="calls",
            query=self.get_query_vector(query=query).tolist(),
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="metadata.type", match=MatchValue(value="ESTABLISHED")
                    )
                ]
            ),
            limit=5,
        )
        results = []
        for r in search_result.points:
            results.append(
                {
                    "text": r.payload["chunk_text"],
                    "score": r.score,
                    "metadata": r.payload["metadata"],
                }
            )

        return results
