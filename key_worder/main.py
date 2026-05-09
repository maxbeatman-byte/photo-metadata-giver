import traceback

from piexif import InvalidImageDataError

from file_service import add_metadata_to_file, get_images
from gpt_service import send_photo_to_openai

print("Start")

image_paths = get_images()

print("Images found: ", len(image_paths))
for index, i in enumerate(image_paths):
    i2 = str(i)
    fname = i.name
    try:
        result = send_photo_to_openai(i2)
        add_metadata_to_file(
            i,
            result.get("TITLE"),
            result.get("DESCRIPTION"),
            result.get("KEYWORDS"),
        )
        print(f"completed {index + 1} from {len(image_paths)} ({fname})")
    except InvalidImageDataError as e:
        print(f"[{fname}] помилка JPEG/EXIF: {e}")
    except Exception as e:
        print(f"[{fname}] {type(e).__name__}: {e}")
        traceback.print_exc()
