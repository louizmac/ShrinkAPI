<div align="center">

# ShrinkAPI

<p>
  A lightweight, open-source image compression REST API.
  <br>
  Fast, simple, and fully self-hosted.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-REST_API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-black?style=flat-square" alt="License">
</p>

</div>

---

## Overview

ShrinkAPI is a simple, self-hosted REST API that allows developers to compress and convert images without relying on external services.

Images are processed locally in memory and returned directly to the client.

## Features

- Image compression with adjustable quality
- JPEG, PNG, WebP, BMP and TIFF input support
- JPEG, PNG and WebP output formats
- Automatic EXIF orientation correction
- Maximum upload size of 20 MiB
- No database or external API required
- Interactive API documentation
- Fully self-hosted

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/louizmac/ShrinkAPI.git
cd ShrinkAPI
```

**2. Install dependencies**

```bash
python3 -m pip install fastapi uvicorn pillow python-multipart
```

**3. Start the server**

```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive documentation:

`http://127.0.0.1:8000/docs`

## API Reference

### Compress Image

`POST /api/v1/compress`

Upload an image and receive the compressed result.

**Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| file | File | Required | Image to compress |
| quality | Integer | 80 | Compression quality (1–100) |
| output_format | String | webp | Output format: jpeg, png, webp |

**Example Request**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/compress?quality=80&output_format=webp" \
  -F "file=@image.png" \
  --output compressed.webp
```

**Python Example**

```python
import requests

url = "http://127.0.0.1:8000/api/v1/compress"

with open("image.png", "rb") as image:
    response = requests.post(
        url,
        files={"file": image},
        params={
            "quality": 80,
            "output_format": "webp"
        }
    )

response.raise_for_status()

with open("compressed.webp", "wb") as output:
    output.write(response.content)
```

## Supported Formats

| Format | Input | Output |
|--------|-------|--------|
| JPEG | Yes | Yes |
| PNG | Yes | Yes |
| WebP | Yes | Yes |
| BMP | Yes | No |
| TIFF | Yes | No |

## Project Structure

```text
ShrinkAPI/
├── main.py
└── README.md
```

## Notes

- Compression results depend on the original image.
- PNG optimization is lossless and may produce smaller savings.
- JPEG conversion does not preserve transparency.
- The API is intended for local development and trusted environments. Additional security measures are recommended before public deployment.

## License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

  <sub>Built with Python, FastAPI and Pillow.</sub>
  <br>
  <sub>Created by <a href="https://github.com/louizmac">louizmac</a></sub>

</div>
