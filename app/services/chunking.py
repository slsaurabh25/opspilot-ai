def create_chunks(
    text: str,
    chunk_size: int = 40,
    overlap: int = 10,
) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    text_chunks = text.split()
    chunks = []

    step = chunk_size-overlap

    for i in range(0, len(text_chunks), step):
         end = i + chunk_size
         chunk = " ".join(text_chunks[i:i+chunk_size])
         chunks.append(chunk)
         if end >= len(text_chunks):
            break

    return chunks

from dataclasses import dataclass

from app.services.document_parser import DocumentSection

@dataclass
class RunbookChunk:
    section_heading: str
    chunk_index: int
    content: str
    word_count: int

def create_section_chunks(
    sections: list[DocumentSection],
    chunk_size: int = 100,
    overlap: int = 20,
) -> list[RunbookChunk]:

    chunks: list[RunbookChunk] = []

    # Loop through each section.
    for sections_chunk in sections:
        # Call create_chunks() using section.content.
        section_chunks = create_chunks(
            text=sections_chunk.content,
            chunk_size=chunk_size,
            overlap=overlap
        )

        # enumerate() the resulting strings.
        for index, chunk_content in enumerate(section_chunks):
            # Create RunbookChunk for every string.
            runbook_chunk = RunbookChunk(
                section_heading=sections_chunk.heading,
                chunk_index=index,
                content=chunk_content,
                word_count=len(chunk_content.split())
            )
            # Add it to chunks.
            chunks.append(runbook_chunk)

    return chunks