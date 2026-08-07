from pydantic import BaseModel, Field


class RunbookRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=10)
    application: str | None = None


class RunbookAnalysisResponse(BaseModel):
    title: str
    application: str | None
    word_count: int
    chunk_count: int
    chunks: list[str]
    status: str


class UploadedRunbookAnalysisResponse(BaseModel):
    file_name: str
    file_size_bytes: int
    word_count: int
    chunk_count: int
    chunks: list[str]
    status: str

class DocumentSectionResponse(BaseModel):
    heading: str
    content: str
    word_count: int

class RunbookChunkResponse(BaseModel):
    section_heading: str
    chunk_index: int
    content: str
    word_count: int

class DocxAnalysisResponse(BaseModel):
    file_name: str
    section_count: int
    word_count: int
    sections: list[DocumentSectionResponse]
    status: str
    chunk_count: int
    chunks: list[RunbookChunkResponse]
