import subprocess, os, time, re

bore = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\bore.exe"
url_file = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3\bore_url.txt"

# Wait for HTTP server
time.sleep(2)

proc = subprocess.Popen(
    [bore, "local", "8080", "--to", "bore.pub"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

url = None
for i in range(30):
    line = proc.stdout.readline()
    if not line:
        time.sleep(0.3)
        continue
    m = re.search(r'listening at (\S+)', line)
    if m:
        url = f"http://{m.group(1)}/horsh-h5-standalone.html"
        break
    m = re.search(r'bore\.pub:(\d+)', line)
    if m:
        url = f"http://bore.pub:{m.group(1)}/horsh-h5-standalone.html"
        break

if url:
    with open(url_file, 'w') as f:
        f.write(url)
    print(f"URL:{url}")
else:
    with open(url_file, 'w') as f:
        f.write("FAILED")
    print("FAILED")

while True:
    time.sleep(60)
