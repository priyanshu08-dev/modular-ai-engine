from typing import Any

from app.retrieval.models import RetrievedChunk


class RetrievalMapper:
    """
    Transforms raw vector store output into domain models and computes
    normalized similarity scores.
    """

    @staticmethod
    def _distance_to_similarity_score(distance: float) -> float:
        """
        Converts raw distance metric (e.g. L2/Euclidean distance from ChromaDB)
        into a normalized similarity score between 0.0 and 1.0.
        """
        if distance < 0:
            return 0.0
        return round(1.0 / (1.0 + distance), 4)

    @classmethod
    def from_chroma_response(
        cls,
        raw_response: dict[str, Any],
        score_threshold: float = 0.0,
    ) -> list[RetrievedChunk]:
        """
        Parses raw ChromaDB query result dict and converts records into RetrievedChunk models.
        """
        ids = raw_response.get("ids", [[]])[0]
        documents = raw_response.get("documents", [[]])[0]
        metadatas = raw_response.get("metadatas", [[]])[0]
        distances = raw_response.get("distances", [[]])[0]

        retrieved_chunks: list[RetrievedChunk] = []

        for embedding_id, document_content, metadata, distance in zip(
            ids, documents, metadatas, distances, strict=False
        ):
            score = cls._distance_to_similarity_score(distance)

            if score < score_threshold:
                continue

            chunk_id = metadata.get("chunk_id", embedding_id)
            document_id = metadata.get("document_id", "unknown")

            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    content=document_content,
                    score=score,
                    metadata=metadata,
                )
            )

        retrieved_chunks.sort(key=lambda c: c.score, reverse=True)
        return retrieved_chunks
