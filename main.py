"""
PDF to Markdown Converter API

A FastAPI application that converts PDF files to Markdown format.
Extracts text, preserves basic formatting, and handles images.

Author: @msi-shamim (im.msishamim@gmail.com)
"""

import io
import base64
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


app = FastAPI(
    title="PDF to Markdown Converter",
    description="Convert PDF documents to Markdown format with text and image extraction",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_with_formatting(page: fitz.Page) -> str:
    """
    Extract text from a PDF page while attempting to preserve formatting.

    Uses block-level extraction to maintain paragraph structure and
    detect potential headings based on font size.

    Args:
        page: A PyMuPDF page object

    Returns:
        Extracted text with basic Markdown formatting applied
    """
    blocks = page.get_text("dict")["blocks"]
    markdown_content = []

    for block in blocks:
        if block["type"] == 0:  # Text block
            block_text = []
            for line in block.get("lines", []):
                line_text = ""
                max_font_size = 0

                for span in line.get("spans", []):
                    text = span.get("text", "")
                    font_size = span.get("size", 12)
                    font_flags = span.get("flags", 0)

                    max_font_size = max(max_font_size, font_size)

                    # Apply bold formatting if font is bold (flag bit 2^4 = 16)
                    is_bold = font_flags & 16
                    # Apply italic formatting if font is italic (flag bit 2^1 = 2)
                    is_italic = font_flags & 2

                    if is_bold and is_italic:
                        text = f"***{text}***"
                    elif is_bold:
                        text = f"**{text}**"
                    elif is_italic:
                        text = f"*{text}*"

                    line_text += text

                if line_text.strip():
                    block_text.append((line_text.strip(), max_font_size))

            # Convert block text to markdown with heading detection
            if block_text:
                avg_font_size = sum(fs for _, fs in block_text) / len(block_text)
                combined_text = " ".join(text for text, _ in block_text)

                # Heuristic: larger fonts are likely headings
                if avg_font_size > 18:
                    markdown_content.append(f"# {combined_text}")
                elif avg_font_size > 14:
                    markdown_content.append(f"## {combined_text}")
                elif avg_font_size > 12:
                    markdown_content.append(f"### {combined_text}")
                else:
                    markdown_content.append(combined_text)

    return "\n\n".join(markdown_content)


def extract_images_as_base64(page: fitz.Page, page_number: int) -> list[dict]:
    """
    Extract all images from a PDF page and encode them as base64.

    Args:
        page: A PyMuPDF page object
        page_number: The page number for reference in output

    Returns:
        List of dictionaries containing image data and metadata
    """
    images = []
    image_list = page.get_images(full=True)

    for img_index, img_info in enumerate(image_list):
        xref = img_info[0]

        try:
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            encoded_image = base64.b64encode(image_bytes).decode("utf-8")

            images.append({
                "page": page_number,
                "index": img_index,
                "format": image_ext,
                "base64": encoded_image,
            })
        except Exception:
            # Skip images that cannot be extracted
            continue

    return images


def convert_pdf_to_markdown(
    pdf_bytes: bytes,
    include_images: bool = False,
    embed_images: bool = False
) -> dict:
    """
    Convert a PDF document to Markdown format.

    Processes each page of the PDF, extracting text with formatting
    and optionally extracting images.

    Args:
        pdf_bytes: Raw bytes of the PDF file
        include_images: Whether to extract and include images
        embed_images: Whether to embed images as base64 data URIs in markdown

    Returns:
        Dictionary containing markdown content and optional image data
    """
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse PDF: {str(error)}"
        )

    markdown_pages = []
    all_images = []

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]

        # Add page separator for multi-page documents
        if page_number > 0:
            markdown_pages.append(f"\n---\n\n*Page {page_number + 1}*\n")

        page_markdown = extract_text_with_formatting(page)

        if include_images:
            page_images = extract_images_as_base64(page, page_number + 1)

            if embed_images and page_images:
                # Embed images directly in markdown
                for img in page_images:
                    image_markdown = f"\n\n![Image {img['index'] + 1} from page {img['page']}](data:image/{img['format']};base64,{img['base64']})\n"
                    page_markdown += image_markdown
            else:
                all_images.extend(page_images)

        markdown_pages.append(page_markdown)

    pdf_document.close()

    final_markdown = "\n\n".join(markdown_pages)

    result = {"markdown": final_markdown}

    if include_images and not embed_images:
        result["images"] = all_images

    return result


@app.post("/convert", response_class=JSONResponse)
async def convert_pdf(
    file: UploadFile = File(..., description="PDF file to convert"),
    include_images: bool = Query(
        default=False,
        description="Extract and include images from the PDF"
    ),
    embed_images: bool = Query(
        default=False,
        description="Embed images as base64 data URIs in the markdown"
    )
) -> dict:
    """
    Convert a PDF file to Markdown.

    Returns JSON with markdown content and optionally extracted images.
    Use include_images=true to extract images separately.
    Use embed_images=true to embed images directly in the markdown.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be a PDF"
        )

    pdf_content = await file.read()
    result = convert_pdf_to_markdown(
        pdf_content,
        include_images=include_images,
        embed_images=embed_images
    )

    return {
        "filename": file.filename,
        "markdown": result["markdown"],
        "images": result.get("images", []),
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy", "service": "pdf-to-markdown"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
