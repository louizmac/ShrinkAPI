from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps, UnidentifiedImageError
from io import BytesIO

app = FastAPI(
    title="ShrinkAPI",
    description="A simple self-hosted image compression API",
    version="1.0.0"
)

SUPPORTED_FORMATS = {
    "JPEG", "PNG", "WEBP", "BMP", "TIFF"
}

@app.get("/")
def home():
    return {
        "name": "ShrinkAPI",
        "version": "1.0.0",
        "status": "online"
    }


@app.post("/api/v1/compress")
async def compress_image(
    file: UploadFile = File(...),
    quality: int = 80,
    output_format: str = "webp"
):
    if not 1 <= quality <= 100:
        raise HTTPException(400, "Quality must be between 1 and 100")

    output_format = output_format.lower()

    if output_format not in ["jpeg", "png", "webp"]:
        raise HTTPException(400, "Unsupported output format")

    original = await file.read()

    if len(original) > 20 * 1024 * 1024:
        raise HTTPException(413, "File too large")

    try:
        image = Image.open(BytesIO(original))

        if image.format not in SUPPORTED_FORMATS:
            raise HTTPException(415, "Unsupported image format")

        image = ImageOps.exif_transpose(image)
        image.load()

        if output_format == "jpeg":
            image = image.convert("RGB")

        output = BytesIO()

        if output_format == "png":
            image.save(output, format="PNG", optimize=True)

        else:
            image.save(
                output,
                format=output_format.upper(),
                quality=quality,
                optimize=True
            )

        output.seek(0)

        media_types = {
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp"
        }

        return StreamingResponse(
            output,
            media_type=media_types[output_format],
            headers={
                "X-Original-Size": str(len(original)),
                "X-Compressed-Size": str(output.getbuffer().nbytes),
                "Content-Disposition": f'attachment; filename="compressed.{output_format}"'
            }
        )

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(400, "Invalid or corrupted image")