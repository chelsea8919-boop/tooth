import subprocess, os, time, json

WORK = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3"
LOG = os.path.join(WORK, "vercel_log.txt")

node = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0\node.exe"
vercel_js = r"C:\Users\Ms.赵\.workbuddy\binaries\node\workspace\node_modules\vercel\dist\index.js"

with open(LOG, 'w') as log:
    log.write("Installing vercel...\n")
    log.flush()
    
    # Install vercel
    npm = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0\node_modules\npm\bin\npm-cli.js"
    proc = subprocess.Popen(
        [node, npm, "install", "vercel", "--save-dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=WORK,
        env={**os.environ, "PATH": r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0;" + os.environ.get("PATH", "")}
    )
    for line in iter(proc.stdout.readline, ''):
        log.write(line)
        log.flush()
    proc.wait()
    log.write(f"\nInstall exit: {proc.returncode}\n")
    log.flush()
    
    # Now try vercel deploy
    if os.path.exists(vercel_js):
        log.write("\nDeploying with vercel...\n")
        log.flush()
        
        deploy_dir = WORK  # root with index.html
        proc2 = subprocess.Popen(
            [node, vercel_js, "deploy", "--prod", "--yes", deploy_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=WORK,
            env={**os.environ, "PATH": r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0;" + os.environ.get("PATH", "")}
        )
        for line in iter(proc2.stdout.readline, ''):
            log.write(line)
            log.flush()
            if 'https://' in line:
                url = line.strip()
                print(f"VERCEL_URL:{url}")
        proc2.wait()
        log.write(f"\nDeploy exit: {proc2.returncode}\n")
    else:
        log.write("vercel_js not found!\n")
