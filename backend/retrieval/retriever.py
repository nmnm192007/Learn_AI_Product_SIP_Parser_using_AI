import logging

from qdrant_client.models import FieldCondition, Filter, MatchValue
from retrieval.emb_model_loader import ModelLoader
from retrieval.qdrant_client import QdrantVectorDB
from retrieval.query_expander import QueryExpander


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
        self._query_expand = QueryExpander()

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
        Get the query string and encode in the model for converting
        to query vector
        :param query:   str
        :return:  query_vector - encoded using model
        """
        query_vector = self._model.encode(query)
        print("Query Vector Shape :: " + str(query_vector.shape))
        print("Query Vector Length :: " + str(len(query_vector)))
        return query_vector

    # def start_search(self, query: str, top_k: int = 5, min_score=0.4):
    def start_search(self, query: str, top_k: int = 8, min_score=0.55):
        """
        Start the search in the vector database
        :param query: str
        :param top_k: int
        :param min_score: float
        :return:List[Dict[str, str]]
        """

        if not self.check_collections("calls"):
            logging.error("Collections object not found")
            raise ValueError("Collections object not found")

        expanded = self._query_expand.expand(query)
        original_query = expanded["original_query"]
        expanded_query = expanded["expanded_query"]

        print(f"\nOriginal Query :: {original_query}")
        print(f"Expanded Query :: {expanded_query}")

        logging.info("Original_Query :: %s", original_query)
        logging.info("Expanded_Query :: %s", expanded_query)

        search_result = self._client.client.query_points(
            collection_name="calls",
            query=self.get_query_vector(query=expanded_query).tolist(),
            limit=top_k,
        )

        results = []
        print("\n============= SEARCH RESULTS =============")
        for r in search_result.points:
            print("--------------------------------")
            print(f"Score : {r.score}")
            print(f"Chunk : {r.payload['chunk_text'][:120]}")
            print(f"Metadata : {r.payload['metadata']}")

            results.append(
                {
                    "text": r.payload["chunk_text"],
                    "score": r.score,
                    "metadata": r.payload["metadata"],
                }
            )

        print("==========================================")

        return results

    #     # results_enriched = self._format_retrieved_context(results)
    #     # return results_enriched
    #
    # def _format_retrieved_context(results: Dict[str:str]) -> str:
    #     """
    #     Helper function to format the retrieved context
    #     :param results: Dict[str,str]
    #     :return:str
    #     """
    #     context_parts = []
    #
    #     for result in results:
    #         payload = result.payload
    #
    #         context_parts.append(f"""
    #                 Chunk ID: {payload.get("chunk_id")}
    #                 Call ID: {payload.get("call_id")}
    #                 Type: {payload.get("type")}
    #                 Call Status: {payload.get("call_status")}
    #                 Messages: {payload.get("messages")}
    #                 Error: {payload.get("error_text")}
    #                 Error Code: {payload.get("error_code")}
    #                 Duration: {payload.get("session_duration_sec")}
    #         """)
    #
    #     return "\n---\n".join(context_parts)
