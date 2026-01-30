# PDF to Markdown Converter

A FastAPI application that converts PDF documents to Markdown format with text extraction, formatting preservation, and automatic image embedding.

## Features

- **Text Extraction** — Extracts text while preserving paragraph structure
- **Formatting Detection** — Detects bold, italic, and heading styles based on font properties
- **Heading Recognition** — Automatically identifies headings based on font size
- **Multi-page Support** — Handles multi-page PDFs with page separators
- **Image Embedding** — Automatically embeds images as base64 in markdown
- **Web UI** — Astro-based frontend with drag & drop, multi-file upload, and zip download

## Quick Start (Docker)

```bash
docker compose up -d
```

| Service | Port | URL |
|---------|------|-----|
| API | 8888 | http://localhost:8888 |
| UI | 4325 | http://localhost:4325 |

## Manual Installation

```bash
pip install -r requirements.txt
python main.py
```

Server runs at `http://localhost:8000`

## API Endpoint

### `POST /convert`

Converts PDF to Markdown. Returns JSON with markdown content and optionally extracted images.

```bash
# Basic conversion
curl -X POST -F "file=@document.pdf" http://localhost:8888/convert

# With images embedded in markdown
curl -X POST -F "file=@document.pdf" "http://localhost:8888/convert?include_images=true&embed_images=true"
```

**Response:**
```json
{
  "filename": "document.pdf",
  "markdown": "# Heading\n\nContent...",
  "images": []
}
```

**Query Parameters:**
- `include_images` (bool) — Extract images from PDF
- `embed_images` (bool) — Embed images as base64 data URIs in markdown

### `GET /health`

Health check endpoint.

```bash
curl http://localhost:8888/health
```

## Web UI

The UI at `http://localhost:4325` provides:
- Drag & drop or click to upload
- Multiple file upload support
- Automatic image embedding
- Downloads as incremental zip files (`1-pdf2md.zip`, `2-pdf2md.zip`, etc.)

## Dependencies

- FastAPI
- Uvicorn
- PyMuPDF (fitz)
- Pillow
- python-multipart

## License

MIT

## Author

GitHub: [@msi-shamim](https://github.com/msi-shamim)
Email: im.msishamim@gmail.com
