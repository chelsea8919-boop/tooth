import subprocess, os, time

node = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0\node.exe"
script = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\start_lt.js"

env = os.environ.copy()
env["NODE_PATH"] = r"C:\Users\Ms.赵\.workbuddy\binaries\node\workspace\node_modules"

proc = subprocess.Popen([node, script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)

# Wait for URL file
url_file = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\tunnel_url.txt"
for i in range(15):
    time.sleep(1)
    if os.path.exists(url_file):
        with open(url_file) as f:
            content = f.read().strip()
        if content and content != 'connecting...':
            print(f"URL:{content}")
            break

# Keep alive
while True:
    time.sleep(60)
