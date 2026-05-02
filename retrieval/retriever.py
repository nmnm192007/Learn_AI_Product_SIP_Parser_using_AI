from qdrant_client.models import FieldCondition, Filter, MatchValue
from retrieval.emb_model_loader import ModelLoader
from retrieval.qdrant_client import QdrantVectorDB


class Retriever:
    """
    Retriever class to retrieve the most similar calls
    from the vector database
    using the vector database
    based on the query

    Args:
        db (QdrantVectorDB): QdrantVectorDB instance
        model (SentenceTransformer): SentenceTransformer instance
        query (str): query string
    Returns:
        list: list of most similar calls

    """

    def __init__(self, db):
        """
        Initialize the Retriever class
        :param db:
        :param model:

        """
        self._model = ModelLoader.get_model()
        self._client = db

    def check_collections(self, c_obj):
        """
        Check if the collection exists in the vector database
        :param c_obj: collection_name
        :return: boolean
        """
        collection_existing = self._client.client.get_collections().collections
        existing_col = [col.name for col in collection_existing]

        if c_obj not in existing_col:
            print("Collections Not Found ::" + str(c_obj))
            raise ValueError(f"Collection {c_obj} not found in qdrant")
        return True

    def get_query_vector(self, query: str):
        """
        Get the query string and encode in the model for convering to query vector
        :param query:   str
        :return:  query_vector - encoded using model
        """
        query_vector = self._model.encode(query)
        print("Query Vector Shape :: " + str(query_vector.shape))
        print("Query Vector Length :: " + str(len(query_vector)))
        return query_vector

    def start_search(self, query: str, top_k: int = 5):
        """
        Start the search in the vector database
        :param query: str
        :param top_k: int
        :return:List[Dict[str, str]]
        """

        if not self.check_collections("calls"):
            raise ValueError("Collections object not found")

        search_result = self._client.client.query_points(
            collection_name="calls",
            query=self.get_query_vector(query=query).tolist(),
            limit=top_k,
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
