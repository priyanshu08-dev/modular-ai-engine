from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.chunking.models import Chunk, ChunkMetadata, ChunkingResult
from app.chunking.strategies.base import BaseChunkingStrategy
from app.config.settings import settings
from app.document.models import Document


class RecursiveChunkingStrategy(BaseChunkingStrategy):
    """
    Chunk documents using LangChain's
    RecursiveCharacterTextSplitter.
    """

    def __init__(self) -> None:

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=settings.CHUNK_SEPARATORS,
            keep_separator=settings.KEEP_SEPARATOR,
            is_separator_regex=settings.IS_SEPARATOR_REGEX,
        )

    def split(
        self,
        document: Document,
    ) -> list[Chunk]:

        texts = self._splitter.split_text(
            document.content,
        )

        chunks: list[Chunk] = []

        current_position = 0

        for index, text in enumerate(texts):
            start = document.content.find(
                text,
                current_position,
            )

            end = start + len(text)

            current_position = end

            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    document_id=document.document_id,
                    document_type=document.document_type,
                    chunk_index=index,
                    content=text,
                    metadata=ChunkMetadata(),
                    start_char=start,
                    end_char=end,
                )
            )

        return ChunkingResult(
            document_id=document.document_id,
            strategy_name=self.__class__.__name__,
            chunks=chunks,
        )
