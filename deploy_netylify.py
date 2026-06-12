import urllib.request, json, os, zipfile, io

proj_dir = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3"
html_file = os.path.join(proj_dir, "horsh-h5-standalone.html")
LOG = os.path.join(proj_dir, "netlify_log.txt")

with open(LOG, 'w') as log:
    log.write("=== Netlify Deploy ===\n")
    
    # Create zip in memory
    log.write("Creating zip...\n")
    log.flush()
    
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        with open(html_file, 'rb') as f:
            zf.writestr("index.html", f.read())
    zip_buf.seek(0)
    
    zip_data = zip_buf.read()
    log.write(f"Zip size: {len(zip_data)//1024} KB\n")
    log.flush()
    
    # Deploy to netlify (no auth needed for first deploy)
    boundary = b'----NetlifyBoundary12345'
    body = b''
    body += b'--' + boundary + b'\r\n'
    body += b'Content-Disposition: form-data; name="file"; filename="site.zip"\r\n'
    body += b'Content-Type: application/zip\r\n\r\n'
    body += zip_data
    body += b'\r\n--' + boundary + b'--\r\n'
    
    log.write("Posting to netlify API...\n")
    log.flush()
    
    try:
        req = urllib.request.Request(
            'https://api.netlify.com/api/v1/sites',
            data=body,
            headers={
                'Content-Type': 'multipart/form-data; boundary=' + boundary.decode(),
                'User-Agent': 'Mozilla/5.0'
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        log.write(f"Response: {json.dumps(result, indent=2)}\n")
        
        if 'url' in result:
            url = result['url']
            print(f"NETLIFY_URL:{url}")
        elif 'name' in result:
            site_name = result['name']
            url = f"https://{site_name}.netlify.app"
            print(f"NETLIFY_URL:{url}")
            
    except Exception as e:
        log.write(f"FAIL: {e}\n")
        print(f"ERROR: {e}")
