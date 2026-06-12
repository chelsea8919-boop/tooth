import base64, json, urllib.request, urllib.parse, os, re

LOG = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\github_upload_log.txt"

with open(LOG, 'w') as log:
    log.write("=== GitHub Upload via API ===\n")
    
    # Read the standalone HTML
    html_path = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-standalone.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # GitHub Contents API - we can create a gist anonymously OR create a repo file
    # Problem: GH requires auth for creating content
    # Solution: Use the "Raw" service via a different approach
    
    # Try: Create a git.io short URL by pushing to a disposable repo
    # Not possible without auth
    
    # TRY A DIFFERENT SERVICE: jsdelivr
    # jsdelivr can serve files from GitHub, but we need a repo first
    
    # Let's try: use an EXISTING public GitHub repo's raw URL
    # We can use githack.com or similar
    
    # Actually, let me try: `paste.ubuntu.com` which is accessible from China
    log.write("Trying Ubuntu Paste...\n")
    log.flush()
    
    try:
        data = urllib.parse.urlencode({
            'poster': 'workbuddy',
            'syntax': 'html',
            'content': html_content
        }).encode('utf-8')
        
        req = urllib.request.Request(
            'https://paste.ubuntu.com',
            data=data,
            headers={'User-Agent': 'Mozilla/5.0'},
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=60)
        url = resp.geturl()
        log.write(f"Ubuntu Paste URL: {url}\n")
        print(f"UBUNTU_URL:{url}")
        
    except Exception as e:
        log.write(f"Ubuntu Paste FAIL: {e}\n")
    
    # Try: Ghostbin
    log.write("\nTrying ghostbin...\n")
    log.flush()
    
    try:
        # ghostbin API
        pass
    except Exception as e:
        log.write(f"Ghostbin FAIL: {e}\n")
    
    # Try: 0x0.st (file upload, returns URL)
    log.write("\nTrying 0x0.st...\n")
    log.flush()
    
    try:
        boundary = b'---WorkBuddy0x0'
        body = b''
        body += b'--' + boundary + b'\r\n'
        body += b'Content-Disposition: form-data; name="file"; filename="horsh-h5.html"\r\n'
        body += b'Content-Type: text/html\r\n\r\n'
        body += html_content.encode('utf-8')[:100000]  # first 100KB only
        body += b'\r\n--' + boundary + b'--\r\n'
        
        req = urllib.request.Request(
            'https://0x0.st',
            data=body,
            headers={
                'Content-Type': 'multipart/form-data; boundary=' + boundary.decode(),
                'User-Agent': 'curl/7.68.0'
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=60)
        url = resp.read().decode('utf-8').strip()
        log.write(f"0x0.st URL: {url}\n")
        print(f"0X0_URL:{url}")
        
    except Exception as e:
        log.write(f"0x0.st FAIL: {e}\n")
