from pydantic import BaseModel, ConfigDict


class DocumentMetadataResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    filename: str
    extension: str
    mime_type: str

    size: int

    page_count: int | None = None

    character_count: int
    word_count: int


class DocumentResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    document_id: str
    
    document_type: str

    content: str

    metadata: DocumentMetadataResponse
