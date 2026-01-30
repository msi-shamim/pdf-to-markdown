# PDF to Markdown Converter

A FastAPI application that converts PDF documents to Markdown format with text extraction, formatting preservation, and optional image extraction.

## Features

- **Text Extraction** — Extracts text while preserving paragraph structure
- **Formatting Detection** — Detects bold, italic, and heading styles based on font properties
- **Heading Recognition** — Automatically identifies headings based on font size
- **Multi-page Support** — Handles multi-page PDFs with page separators
- **Image Extraction** — Optionally extracts images as base64 (separate or embedded)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start the server:

```bash
python main.py
```

Server runs at `http://localhost:8000`

### API Endpoints

#### `POST /convert`
Simple conversion — returns plain markdown text.

```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/convert
```

#### `POST /convert/full`
Full conversion — returns JSON with markdown and optional images.

```bash
# Basic
curl -X POST -F "file=@document.pdf" http://localhost:8000/convert/full

# With images extracted separately
curl -X POST -F "file=@document.pdf" "http://localhost:8000/convert/full?include_images=true"

# With images embedded in markdown
curl -X POST -F "file=@document.pdf" "http://localhost:8000/convert/full?embed_images=true"
```

#### `GET /health`
Health check endpoint.

```bash
curl http://localhost:8000/health
```

### Interactive Documentation

Swagger UI available at `http://localhost:8000/docs`

## Dependencies

- FastAPI
- Uvicorn
- PyMuPDF (fitz)
- Pillow
- python-multipart

## License

MIT
