import json, urllib.request, os, sys

LOG = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\gist_log.txt"

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)

log("Starting...")

html_path = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-standalone.html"

log(f"Reading {html_path}")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

size_mb = len(content.encode("utf-8")) / (1024 * 1024)
log(f"File size: {size_mb:.1f} MB")

# GitHub Gist might have issues with large files
# Try with compression or use a different approach
# Let's try posting without the full content first to test

log("Testing API with small payload...")
try:
    test_data = json.dumps({
        "description": "test",
        "public": False,
        "files": {"test.txt": {"content": "hello"}}
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "https://api.github.com/gists",
        data=test_data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WorkBuddy"
        },
        method="POST"
    )
    resp = urllib.request.urlopen(req, timeout=30)
    log(f"Test OK: {resp.status}")
except Exception as e:
    log(f"Test FAIL: {e}")
    sys.exit(1)

log("Now posting full file...")
try:
    data = json.dumps({
        "description": "豪士面包H5 - 捏捏乐互动页面",
        "public": True,
        "files": {
            "horsh-h5.html": {"content": content}
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "https://api.github.com/gists",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "WorkBuddy"
        },
        method="POST"
    )
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read())
    raw_url = result["files"]["horsh-h5.html"]["raw_url"]
    
    with open(r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\gist_url.txt", "w") as f:
        f.write(raw_url)
    
    log(f"SUCCESS: {raw_url}")
    
except Exception as e:
    log(f"FULL POST FAIL: {e}")
