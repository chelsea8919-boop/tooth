import os

src = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-standalone.html"
dst = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-min.html"

with open(src, 'r', encoding='utf-8') as f:
    lines = f.readlines()

orig_size = sum(len(l.encode('utf-8')) for l in lines)

# Simple: strip leading/trailing whitespace from each line, remove blank lines
minified = []
for line in lines:
    stripped = line.strip()
    if stripped:
        minified.append(stripped)

result = '\n'.join(minified)
new_size = len(result.encode('utf-8'))

with open(dst, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"{orig_size/1024:.0f}KB -> {new_size/1024:.0f}KB")
