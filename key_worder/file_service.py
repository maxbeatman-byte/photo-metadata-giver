import sys
from pathlib import Path

import piexif

from iptc_metadata import add_stock_iptc_metadata


def _image_search_dir() -> Path:
    # PyInstaller: cwd is often wrong (e.g. / or ~ when opened from Finder); use the exe folder.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd()


def get_images() -> list[Path]:
    current_dir = _image_search_dir()
    image_extensions = {".jpg", ".jpeg"}

    images = [
        file for file in current_dir.iterdir()
        if file.is_file() and file.suffix.lower() in image_extensions
    ]

    return images


def add_metadata_to_file(
        file_path: Path,
        title: str,
        description: str,
        keywords: list[str] | str
) -> None:
    # Normalize keywords to a list of non-empty, stripped strings
    if isinstance(keywords, str):
        normalized_keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    elif isinstance(keywords, list):
        if len(keywords) == 1 and isinstance(keywords[0], str) and "," in keywords[0]:
            normalized_keywords = [k.strip() for k in keywords[0].split(",") if k.strip()]
        else:
            normalized_keywords = [str(k).strip() for k in keywords if str(k).strip()]
    else:
        normalized_keywords = []

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    if file_path.suffix.lower() not in [".jpg", ".jpeg"]:
        raise ValueError("Only JPG/JPEG files are supported")

    # Load existing EXIF if present; otherwise start with an empty template
    try:
        exif_dict = piexif.load(str(file_path))
    except Exception:
        exif_dict = {
            "0th": {},
            "Exif": {},
            "GPS": {},
            "Interop": {},
            "1st": {},
            "thumbnail": None,
        }
    else:
        # piexif.dump() re-embeds "thumbnail" as JPEG; many files store TIFF or invalid previews.
        exif_dict["thumbnail"] = None
        exif_dict["1st"] = {}

    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = (title or "").encode("utf-8")

    exif_dict["Exif"][piexif.ExifIFD.UserComment] = (
        b"ASCII\x00\x00\x00" + (description or "").encode("utf-8")
    )

    keywords_string = ", ".join(normalized_keywords)
    exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords_string.encode("utf-16le")

    exif_bytes = piexif.dump(exif_dict)

    add_stock_iptc_metadata(file_path, title, description, normalized_keywords)

    piexif.insert(exif_bytes, str(file_path))
