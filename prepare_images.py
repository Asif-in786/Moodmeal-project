# prepare_images.py
# Usage: put your aurals_images.json (or multiple JSON files) in this folder,
# then run: python prepare_images.py
import os, glob, json, base64, io
from PIL import Image

OUT_DIR = "data"
TARGET_SIZE = (160,160)   # change if you want larger images

os.makedirs(OUT_DIR, exist_ok=True)

json_files = glob.glob("*.json")
if not json_files:
    print("No .json files found in current folder. Move your auralens_images.json here.")
    raise SystemExit(1)

total = 0
for jf in json_files:
    print("Processing", jf)
    with open(jf, "r", encoding="utf-8") as f:
        images = json.load(f)   # expects {"happy":[dataURL,...], "sad":[...], ...}
    for label, arr in images.items():
        out_label_dir = os.path.join(OUT_DIR, "train", label)
        os.makedirs(out_label_dir, exist_ok=True)
        for i, dataurl in enumerate(arr):
            try:
                header, b64 = dataurl.split(",", 1)
            except Exception:
                # maybe it's already raw base64 without header
                b64 = dataurl
            try:
                imgdata = base64.b64decode(b64)
                img = Image.open(io.BytesIO(imgdata)).convert("RGB")
                img = img.resize(TARGET_SIZE)
                fname = os.path.join(out_label_dir, f"{os.path.splitext(jf)[0]}_{i:04d}.jpg")
                img.save(fname, quality=85)
                total += 1
            except Exception as e:
                print("Failed to save image", jf, label, i, ":", e)
print(f"Done. Wrote {total} images into {os.path.join(OUT_DIR,'train')}")
