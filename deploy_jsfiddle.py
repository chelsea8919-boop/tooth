import base64, json, urllib.request, os

LOG = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\github_pages_log.txt"

with open(LOG, 'w') as log:
    log.write("=== GitHub Pages Deploy ===\n")
    
    # Create a gist (anonymous, no auth needed for public gists)
    # GitHub removed anonymous gist creation, but let me try...
    
    # Read standalone HTML
    html_path = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\horsh-h5-standalone.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    log.write(f"HTML size: {len(content)} chars\n")
    log.flush()
    
    # Try creating a gist (might work without auth for small files)
    # Actually, GitHub requires auth since 2020
    
    # Try: Use an EXISTING public gist and update it
    # Not possible without auth
    
    # Try: Use a code sharing service that renders HTML
    # 1. codesandbox.io API
    # 2. stackblitz.com API
    # 3. jsfiddle.net API
    
    log.write("\nTrying jsfiddle.net API...\n")
    log.flush()
    
    try:
        # jsfiddle has a simple POST API
        data = urllib.parse.urlencode({
            'title': '豪士面包H5',
            'html': content,
            'css': '',
            'js': '',
            'dtd': 'html 5'
        }).encode('utf-8')
        
        req = urllib.request.Request(
            'https://jsfiddle.net/api/post/latest/save',
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0'
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
        log.write(f"JSFiddle result: {json.dumps(result)}\n")
        
        if 'id' in result:
            url = f"https://jsfiddle.net/{result['id']}/show"
            print(f"JSFIDDLE_URL:{url}")
            
    except Exception as e:
        log.write(f"JSFiddle FAIL: {e}\n")
    
    # Try: codepen.io API
    log.write("\nTrying CodePen API...\n")
    log.flush()
    
    try:
        data = json.dumps({
            'title': '豪士面包H5',
            'html': content[:100000],  # codepen might have limits
            'css': '',
            'js': ''
        }).encode('utf-8')
        
        # CodePen API requires auth, but let me try anonymous
        
    except Exception as e:
        log.write(f"CodePen FAIL: {e}\n")
