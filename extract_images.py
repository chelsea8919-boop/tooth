import re, base64, os

src = 'horsh-h5-standalone.html'
out = 'deploy/index.html'
img_dir = 'deploy/images'
os.makedirs(img_dir, exist_ok=True)

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(data:image/(png|jpeg|jpg|webp|gif);base64,)([A-Za-z0-9+/=\s]+)'
matches = list(re.finditer(pattern, content))
print(f'Found {len(matches)} base64 images')

# Replace from end to start to preserve offsets
for idx, m in enumerate(reversed(matches)):
    mime = m.group(2)
    b64data = m.group(3).replace('\n', '').replace('\r', '').replace(' ', '')
    try:
        img_bytes = base64.b64decode(b64data)
        ext = mime if mime != 'jpeg' else 'jpg'
        filename = f'img_{len(matches)-idx}.{ext}'
        filepath = os.path.join(img_dir, filename)

        with open(filepath, 'wb') as imgf:
            imgf.write(img_bytes)

        # Replace in content
        replacement = f'images/{filename}'
        content = content[:m.start()] + replacement + content[m.end():]
        print(f'  Extracted {filename}: {len(img_bytes)/1024:.1f} KB')
    except Exception as e:
        print(f'  Error on image {len(matches)-idx}: {e}')

with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nDone! Output: {out}')
out_size = os.path.getsize(out)
print(f'Output size: {out_size/1024:.1f} KB ({out_size/1024/1024:.2f} MB)')
