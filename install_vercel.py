import subprocess, os, sys

WORK = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3"
LOG = os.path.join(WORK, "vercel_install_log.txt")

with open(LOG, 'w') as log:
    node = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0\node.exe"
    npm_js = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0\node_modules\npm\bin\npm-cli.js"
    
    log.write(f"Installing vercel to {WORK}\n")
    log.flush()
    
    env = os.environ.copy()
    env["PATH"] = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0;" + env.get("PATH", "")
    
    # Install vercel locally
    proc = subprocess.Popen(
        [node, npm_js, "install", "vercel", "--save-dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=WORK,
        env=env
    )
    
    for line in iter(proc.stdout.readline, ''):
        log.write(line)
        log.flush()
    
    proc.wait(timeout=120)
    log.write(f"\nDone. Exit: {proc.returncode}\n")
    print(f"Done. Exit: {proc.returncode}")
