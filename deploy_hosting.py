import urllib.request, os, json

# Try tiiny.host free upload API
html_path = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-standalone.html"
log_path = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\deploy_log.txt"

with open(log_path, 'w') as log:
    log.write("Trying tiiny.host...\n")
    log.flush()
    
    with open(html_path, 'rb') as f:
        html_data = f.read()
    
    log.write(f"File size: {len(html_data)} bytes\n")
    log.flush()
    
    # Try tiiny.host
    try:
        boundary = '----WorkBuddyBoundary'
        body = b''
        body += f'--{boundary}\r\n'.encode()
        body += b'Content-Disposition: form-data; name="file"; filename="index.html"\r\n'
        body += b'Content-Type: text/html\r\n\r\n'
        body += html_data
        body += f'\r\n--{boundary}--\r\n'.encode()
        
        req = urllib.request.Request(
            'https://api.tiiny.host/v1/upload',
            data=body,
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'User-Agent': 'WorkBuddy'
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        log.write(f"tiiny response: {json.dumps(result, indent=2)}\n")
        
        if 'url' in result:
            print(f"TINY_URL:{result['url']}")
        elif 'link' in result:
            print(f"TINY_URL:{result['link']}")
        else:
            print(f"TINY_RESULT:{json.dumps(result)}")
            
    except Exception as e:
        log.write(f"tiiny.host FAIL: {e}\n")
        
    # Try file.io as backup
    log.write("\nTrying file.io...\n")
    try:
        boundary = '----WorkBuddyBoundary2'
        body = b''
        body += f'--{boundary}\r\n'.encode()
        body += b'Content-Disposition: form-data; name="file"; filename="horsh-h5.html"\r\n'
        body += b'Content-Type: text/html\r\n\r\n'
        body += html_data
        body += f'\r\n--{boundary}--\r\n'.encode()
        
        req = urllib.request.Request(
            'https://file.io',
            data=body,
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'User-Agent': 'WorkBuddy'
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        log.write(f"file.io response: {json.dumps(result, indent=2)}\n")
        
        if 'link' in result:
            print(f"FILEIO_URL:{result['link']}")
            
    except Exception as e:
        log.write(f"file.io FAIL: {e}\n")
