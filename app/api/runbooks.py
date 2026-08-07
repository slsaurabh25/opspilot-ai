from anyio.streams import file
from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.models.runbook import (
    RunbookAnalysisResponse,
    RunbookRequest,
    UploadedRunbookAnalysisResponse, RunbookChunkResponse,
)
from app.services.chunking import (create_chunks)

from app.models.runbook import (
    DocxAnalysisResponse,
    DocumentSectionResponse,
)
from app.services.document_parser import extract_docx_sections

from app.services.chunking import create_section_chunks

MAX_FILE_SIZE_BYTES = 1_000_000

router = APIRouter(
    prefix="/runbooks",
    tags=["Runbooks"],
)

@router.get("/search")
def search_runbooks(query: str):
    return {
        "query": query,
        "message": "Search will be implemented later"
    }


@router.post(
    "/analyze",
    response_model=RunbookAnalysisResponse,
)
def analyze_runbook(
    runbook: RunbookRequest,
    chunk_size: int = Query(default=40, ge=10, le=500),
    overlap: int = Query(default=10, ge=0, le=100),
):
    try:
        # Call create_chunks using chunk_size and overlap.
        chunks = create_chunks(
            text=runbook.content,
            chunk_size=chunk_size,
            overlap=overlap
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Return RunbookAnalysisResponse here.
    return RunbookAnalysisResponse(
        title=runbook.title,
        application=runbook.application,
        word_count=len(runbook.content.split()),
        chunk_count=len(chunks),
        chunks=chunks,
        status="ANALYZED"
    )



@router.post(
    "/upload/analyze",
    response_model=UploadedRunbookAnalysisResponse,
)
async def upload_and_analyze_runbook(
    file: UploadFile = File(...),
    chunk_size: int = Query(default=40, ge=10, le=500),
    overlap: int = Query(default=10, ge=0, le=100),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must have a filename",
        )
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=415,
            detail="Only TXT files are currently supported",
        )
    content_bytes = await file.read()
    if len(content_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum allowed size of {MAX_FILE_SIZE_BYTES} bytes",
        )
    content_text = content_bytes.decode("utf-8")
    if not content_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty or contains only whitespace",
        )
    chunks = create_chunks(
        text=content_text,
        chunk_size=chunk_size,
        overlap=overlap
    )
    return UploadedRunbookAnalysisResponse(
        file_name=file.filename,
        file_size_bytes=len(content_bytes),
        word_count=len(content_text.split()),
        chunk_count=len(chunks),
        chunks=chunks,
        status="ANALYZED"
    )

@router.post(
    "/upload/docx/analyze",
    response_model=DocxAnalysisResponse,
)
async def upload_and_analyze_docx(
    file: UploadFile = File(...),
    chunk_size: int = Query(default=100, ge=10, le=500),
    overlap: int = Query(default=20, ge=0, le=100),
):
    # 1. Verify filename exists.
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must have a filename",
        )

    # 2. Verify that the filename ends with ".docx".
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=415,
            detail="Only DOCX files are currently supported",
        )

    # 3. Read uploaded bytes.
    content_bytes = await file.read()

    # 4. Reject an empty file.
    if not content_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    # 5. Call extract_docx_sections(...).
    try:
        sections = extract_docx_sections(content_bytes)
        runbook_chunks = create_section_chunks(
            sections=sections,
            chunk_size=chunk_size,
            overlap=overlap,
        )
        # inspect_tables(content_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while extracting sections from DOCX file: {str(e)}"
        )

    document_section_responses: list[DocumentSectionResponse] = []

    # 6. Convert each DocumentSection into
    #    DocumentSectionResponse.
    for section in sections:
        document_section_responses.append(
            DocumentSectionResponse(
                heading=section.heading,
                content=section.content,
                word_count=len(section.content.split())
            )
        )

    runbook_chunk_responses: list[RunbookChunkResponse] = []
    for chunk in runbook_chunks:
        runbook_chunk_responses.append(
            RunbookChunkResponse(
                section_heading=chunk.section_heading,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                word_count=chunk.word_count
            )
        )

    # 7. Calculate total word count.
    word_count = sum(section.word_count for section in document_section_responses)

    # 8. Return DocxAnalysisResponse.
    return DocxAnalysisResponse(
        file_name=file.filename,
        sections=document_section_responses,
        word_count=word_count,
        section_count=len(document_section_responses),
        status="ANALYZED",
        chunks=runbook_chunk_responses,
        chunk_count=len(runbook_chunk_responses)
    )
