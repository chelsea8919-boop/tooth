import urllib.request, json, os

# Try ge.tt API - simple file sharing
LOG = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\deploy_v2_log.txt"

with open(LOG, 'w') as log:
    # Try a paste service that renders HTML
    # 1. telegra.ph API (requires domain)
    # 2. Try 0x0.st with smaller file
    
    min_html = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-min.html"
    if not os.path.exists(min_html):
        log.write("min file not found\n")
        # try standalone
        min_html = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-standalone.html"
    
    log.write(f"Using: {min_html}\n")
    log.write(f"Size: {os.path.getsize(min_html)/1024:.0f}KB\n")
    log.flush()
    
    # Try catbox.moe
    log.write("Trying catbox.moe...\n")
    log.flush()
    try:
        with open(min_html, 'rb') as f:
            html_bytes = f.read()
        
        boundary = b'---WorkBuddyFormBoundary12345'
        body = b''
        body += b'--' + boundary + b'\r\n'
        body += b'Content-Disposition: form-data; name="reqtype"; \r\n\r\n'
        body += b'fileupload\r\n'
        body += b'--' + boundary + b'\r\n'
        body += b'Content-Disposition: form-data; name="fileToUpload"; filename="horsh-h5.html"\r\n'
        body += b'Content-Type: text/html\r\n\r\n'
        body += html_bytes
        body += b'\r\n--' + boundary + b'--\r\n'
        
        req = urllib.request.Request(
            'https://catbox.moe/user/api.php',
            data=body,
            headers={
                'Content-Type': 'multipart/form-data; boundary=' + boundary.decode(),
                'User-Agent': 'Mozilla/5.0'
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=120)
        url = resp.read().decode('utf-8').strip()
        log.write(f"catbox result: {url}\n")
        print(f"CATBOX_URL:{url}")
        
    except Exception as e:
        log.write(f"catbox fail: {e}\n")
    
    # Try tmpfiles.org
    log.write("\nTrying tmpfiles.org...\n")
    log.flush()
    try:
        with open(min_html, 'rb') as f:
            html_bytes = f.read()
        
        boundary = b'---WorkBuddyBoundary'
        body = b''
        body += b'--' + boundary + b'\r\n'
        body += b'Content-Disposition: form-data; name="file"; filename="horsh-h5.html"\r\n'
        body += b'Content-Type: text/html\r\n\r\n'
        body += html_bytes
        body += b'\r\n--' + boundary + b'--\r\n'
        
        req = urllib.request.Request(
            'https://tmpfiles.org/api/v1/upload',
            data=body,
            headers={
                'Content-Type': 'multipart/form-data; boundary=' + boundary.decode(),
                'User-Agent': 'Mozilla/5.0'
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        log.write(f"tmpfiles result: {json.dumps(result)}\n")
        if 'data' in result and 'url' in result['data']:
            url = result['data']['url']
            print(f"TMPFILES_URL:{url}")
    except Exception as e:
        log.write(f"tmpfiles fail: {e}\n")
