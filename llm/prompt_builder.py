class PromptBuilder:
    @staticmethod
    def build_prompt(query: str, retrieved_chunks: list) -> str:
        """
        Build a prompt for the LLM
        :param query: str
        :param context: list
        :return: str
        """

        context = "\n".join([chunk["text"] for chunk in retrieved_chunks])

        prompt = f"""
        You are an expert in the field of telecommunication and IT.
        Answer the question based only on the provided context.
        If you don't know the answer, just say that you don't know.
        Don't try to make up an answer.
        If the context is empty, just say that you don't know.

        Context: {context}

        Question: {query}
        
        Instructions:
        - Be precise
        - Explain call flow if needed
        - Mention error codes if present
        
        """
        return prompt
