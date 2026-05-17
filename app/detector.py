import hashlib
from database import save_result


async def analyze_media(file):
    filename = file.filename
    content = await file.read()

    file_hash = hashlib.md5(content).hexdigest()

    if filename.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
        media_type = "image"
    else:
        media_type = "video"

    hash_number = int(file_hash[:8], 16)

    confidence = 70 + (hash_number % 30)

    if confidence > 85:
        prediction = "Likely AI-Generated"
    elif confidence > 75:
        prediction = "Possibly AI-Generated"
    else:
        prediction = "Likely Real"

    save_result(filename, prediction, confidence, media_type)

    return {
        "filename": filename,
        "prediction": prediction,
        "confidence": confidence,
        "media_type": media_type,
        "file_hash": file_hash
    }