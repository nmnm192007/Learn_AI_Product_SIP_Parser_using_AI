class PromptBuilder:
    @staticmethod
    def build_prompt(query: str, retrieved_chunks: list) -> str:
        """
        Build a prompt for the LLM
        :param query: str
        :param context: list
        :return: str
        """

        # context = "\n".join([chunk["text"] for chunk in retrieved_chunks[:2]])
        context = "\n\n".join(
            [f"[LOG {i+1}]\n{c['text']}" for i, c in enumerate(retrieved_chunks)]
        )
        prompt = f"""
            You are a SIP call log analysis assistant.
            
            Answer the user's question using ONLY the provided context.
            
            USER QUESTION:
            {query}
            
            CONTEXT:
            {context}
            
            RULES:
            1. Use only information present in CONTEXT.
            2. Do not invent SIP events, error codes, causes, or call IDs.
            3. If the context does not contain enough information, say:
               "The provided logs do not contain enough information to answer this."
            4. Distinguish SUCCESS from FAILURE exactly as shown in the context.
            5. When discussing failures, provide the error text and error code when available.
            6. If multiple call IDs are present, identify them separately.
            7. Do not claim a call failed merely because a TERMINATED or BYE event exists.
            8. Do not infer customer satisfaction or user experience unless explicitly present.
            9. Keep the answer focused on the user's question.
            
            Answer:
            """

        return prompt


#
# prompt = f"""
#     You are an expert in the field of telecommunication and IT.
#     Answer the question based only on the provided context.
#     If you don't know the answer, just say that you don't know.
#     Don't try to make up an answer.
#     If the context is empty, just say that you don't know.
#
#     Context: {context}
#
#     Question: {query}
#
#     Instructions:
#     - Be precise
#     - Explain call flow if needed
#     - Mention error codes if present
#
#     """

#
# prompt = f"""
# You are a telecom log analysis system.
#
# STRICT RULES:
# - Only use exact information from the context
# - DO NOT infer or assume anything
# - DO NOT introduce new terms not present in context
# - If something is not explicitly present, say "Not found"
#
# Context:
# {context}
#
# Question:
# {query}
#
# Output format:
# - Summary
# - Call Status
# - Errors (if any)
# - Key Messages
# """

#
# prompt = f"""
#    You are a STRICT information extraction system.
#
#    RULES:
#    1. ONLY use exact words from the context
#    2. DO NOT add any new words or assumptions
#    3. DO NOT infer missing steps
#    4. If something is not present, return "Not found"
#    5. DO NOT explain, only extract
#
#    Context:
#    {context}
#
#    Question:
#    {query}
#
#    Return in this format ONLY:
#
#    Summary:
#    <only from context>
#
#    Call Status:
#    <exact value from context>
#
#    Errors:
#    <exact error text or "Not found">
#
#    Messages:
#    <only messages present in context>
#    """
