import re


def extract_doc_header(text):
    """
    Grabs the first few lines to serve as the document title or header.
    """
    lines = text.split("\n")
    header_lines = []
    for line in lines:
        if line.strip().startswith("[SCHEME"):
            break
        if line.strip():
            header_lines.append(line.strip())
        if len(header_lines) >= 4:
            break
    return " | ".join(header_lines)


def chunk_unstructured(text, filename, max_chunk_chars=1200):
    """
    Splits text by [SCHEME ...] headings, prepends doc header for context.
    """
    doc_header = extract_doc_header(text)

    # Split by [SCHEME X]
    section_pattern = r'\n(?=\[SCHEME\s+\d+\])'
    sections = re.split(section_pattern, text)

    chunks = []
    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Don't prepend doc_header to the header block itself
        labeled_section = f"{doc_header}\n\n{section}" if doc_header and "[SCHEME" in section else section

        if len(labeled_section) <= max_chunk_chars:
            chunks.append(labeled_section)
        else:
            # Sub-split long sections by paragraph
            paragraphs = labeled_section.split("\n")
            current = ""
            for para in paragraphs:
                if len(current) + len(para) > max_chunk_chars:
                    if current.strip():
                        chunks.append(current.strip())
                    current = para + "\n"
                else:
                    current += para + "\n"
            if current.strip():
                chunks.append(current.strip())

    return chunks


def classify_doc_type(filename, text=""):
    return "Government Scheme"


def chunk_document(extracted, project_name="Government Schemes Hub"):
    """
    Takes the dict from extract_file() and returns a list of chunk dicts,
    each with the chunk text + metadata for later filtering/citation.
    """
    doc_type_label = classify_doc_type(extracted["filename"], extracted.get("text", ""))

    if extracted["doc_type"] == "unstructured":
        raw_chunks = chunk_unstructured(extracted["text"], extracted["filename"])
    else:
        # Fallback for structured records
        raw_chunks = []
        for record in extracted.get("records", []):
            lines = [f"Document Type: {doc_type_label}", f"Project: {project_name}"]
            for key, val in record.items():
                lines.append(f"{key}: {val}")
            raw_chunks.append("\n".join(lines))

    result = []
    for i, chunk_text in enumerate(raw_chunks):
        result.append({
            "text": chunk_text,
            "filename": extracted["filename"],
            "filetype": extracted["filetype"],
            "doc_type": extracted["doc_type"],
            "document_type": doc_type_label,
            "chunk_id": f"{extracted['filename']}_{i}",
        })
    return result
