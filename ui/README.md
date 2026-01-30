# PDF to Markdown Converter - UI

A modern web interface for converting PDF files to Markdown format with automatic image embedding.

## Features

- Drag & drop or click to upload PDF files
- Multiple file upload support
- Automatic image detection and embedding in markdown
- Downloads as incremental zip files (`1-pdf2md.zip`, `2-pdf2md.zip`, etc.)
- Each PDF converted to separate `.md` file inside the zip
- Dark theme UI

## Tech Stack

- [Astro](https://astro.build) - Web framework
- [JSZip](https://stuk.github.io/jszip/) - Client-side zip generation
- TypeScript

## Getting Started

### Prerequisites

- Node.js 20+
- Docker (optional)

### Development

```sh
npm install
npm run dev
```

The UI will be available at `http://localhost:4321`

### Docker

```sh
docker compose up -d pdf-to-markdown-ui
```

The UI will be available at `http://localhost:4325`

## API

The UI connects to the PDF to Markdown API running at `http://localhost:8888`. Make sure the API is running before using the UI.

## Version

1.1.0

## License

MIT License - see [LICENSE.md](LICENSE.md)

## Author

GitHub: [@msishamim](https://github.com/msishamim)
Email: im.msishamim@gmail.com
