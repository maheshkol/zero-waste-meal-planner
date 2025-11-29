from PIL import Image
import pytesseract
from pyzbar.pyzbar import decode

BARCODE_DB = {
    "0123456789012": {"name": "Milk", "unit": "liters", "default_qty": 1},
}

def parse_pantry_image(filepath: str):
    items = []
    img = Image.open(filepath)
    codes = decode(img)
    for c in codes:
        barcode = c.data.decode('utf-8')
        if barcode in BARCODE_DB:
            items.append({**BARCODE_DB[barcode], "detected_by": "barcode"})
        else:
            items.append({"name": f"Unknown barcode {barcode}", "detected_by": "barcode"})
    text = pytesseract.image_to_string(img)
    keywords = ["milk", "eggs", "chicken", "tomato", "spinach", "onion", "rice", "flour", "butter"]
    lowered = text.lower()
    for k in keywords:
        if k in lowered:
            items.append({"name": k.capitalize(), "unit": "pcs" if k in ["eggs","tomato","onion"] else "qty", "detected_by": "ocr"})
    seen = set()
    deduped = []
    for it in items:
        key = (it.get("name"), it.get("detected_by"))
        if key in seen: continue
        seen.add(key)
        deduped.append(it)
    return deduped
