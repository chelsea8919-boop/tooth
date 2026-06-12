import base64, re, os

WORK = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3"
HTML_IN = os.path.join(WORK, "horsh-h5.html")
HTML_OUT = os.path.join(WORK, "horsh-h5-standalone.html")

IMAGES = [
    "8f1999331a8b039c028a35c539022c5.png",
    "f72f38f06528a7454f2799517444ee5.png",
    "产品正面图.png",
    "豪士logo.png",
    "黄油面包.png",
    "奶香型.png",
]

with open(HTML_IN, "r", encoding="utf-8") as f:
    html = f.read()

for img_name in IMAGES:
    img_path = os.path.join(WORK, img_name)
    if not os.path.exists(img_path):
        print(f"WARN: {img_name} not found, skipping")
        continue

    with open(img_path, "rb") as f:
        img_data = f.read()

    b64 = base64.b64encode(img_data).decode("ascii")
    ext = os.path.splitext(img_name)[1].lower().lstrip(".")
    mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
    data_uri = f"data:{mime};base64,{b64}"

    # Replace all occurrences of this image filename in src attributes
    html = html.replace(f'src="{img_name}"', f'src="{data_uri}"')
    html = html.replace(f"src='{img_name}'", f"src='{data_uri}'")
    # Also handle url() in CSS
    html = html.replace(f'url("{img_name}")', f'url("{data_uri}")')
    html = html.replace(f"url('{img_name}')", f"url('{data_uri}')")

    print(f"OK: {img_name} ({len(img_data)} bytes -> {len(b64)} chars)")

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html)

size_kb = os.path.getsize(HTML_OUT) / 1024
print(f"\nDONE: {HTML_OUT} ({size_kb:.0f} KB)")
