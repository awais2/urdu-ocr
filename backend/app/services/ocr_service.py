"""Gemini vision OCR service for Urdu Nastaliq text."""
import google.generativeai as genai

from app.config import get_settings

OCR_PROMPT = (
    "You are an expert Urdu OCR system specialized in Nastaliq script. "
    "Transcribe ALL Urdu text visible in this newspaper image exactly as written.\n\n"
    "Rules:\n"
    "1. Preserve reading order: headline first, then body text. "
    "For multi-column body text, read columns right-to-left (Urdu order).\n"
    "2. Output ONLY the Urdu text. No translation, no commentary.\n"
    "3. Keep paragraph breaks where they appear in the original.\n"
    "4. Skip decorative masthead calligraphy, phone numbers, and web addresses.\n"
    "5. If a word is unclear, give your best reading; never insert placeholders.\n"
    "6. Do not add Markdown formatting."
)

_settings = get_settings()
genai.configure(api_key=_settings.gemini_api_key)
_model = genai.GenerativeModel("gemini-2.5-flash")

async def extract_urdu_text(base64_image: str) -> str:
    response = await _model.generate_content_async(
        [
            OCR_PROMPT,
            {"mime_type": "image/jpeg", "data": base64_image},
        ],
        generation_config={"temperature": 0, "max_output_tokens": 8192},
    )
    return (response.text or "").strip()