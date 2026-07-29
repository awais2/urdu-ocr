"""
Image preprocessing for Urdu Nastaliq newspaper OCR.

Kept deliberately LLM-friendly: grayscale + upscale + denoise + CLAHE.
Hard binarization is avoided because vision LLMs perform better on
natural-looking, high-contrast grayscale images.
"""
import base64

import cv2
import numpy as np


def decode_image_bytes(data: bytes) -> np.ndarray:
    """Decode raw upload bytes into a BGR image. Handles GIF via first frame."""
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Unsupported or corrupted image file")
    return img


def crop_masthead(img: np.ndarray, ratio: float = 0.18) -> np.ndarray:
    """Remove the decorative newspaper banner from the top of the page."""
    h = img.shape[0]
    return img[int(h * ratio):, :]


def preprocess(
    data: bytes,
    remove_masthead: bool = True,
    masthead_ratio: float = 0.18,
    upscale_threshold: int = 2500,
) -> np.ndarray:
    """Full preprocessing pipeline: crop -> gray -> upscale -> denoise -> CLAHE."""
    img = decode_image_bytes(data)

    if remove_masthead:
        img = crop_masthead(img, masthead_ratio)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    if max(h, w) < upscale_threshold:
        gray = cv2.resize(gray, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)

    gray = cv2.fastNlMeansDenoising(gray, h=10)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


def to_base64_jpeg(img: np.ndarray, quality: int = 92) -> str:
    """Encode a processed image as a base64 JPEG string for the vision API."""
    ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise ValueError("JPEG encoding failed")
    return base64.b64encode(buf).decode("utf-8")
