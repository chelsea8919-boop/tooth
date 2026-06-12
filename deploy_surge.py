import subprocess, os, time, shutil

proj_dir = r"C:\Users\Ms.赵\WorkBuddy\2026-05-29-task-3"
deploy_dir = os.path.join(proj_dir, "deploy")
os.makedirs(deploy_dir, exist_ok=True)
shutil.copy2(os.path.join(proj_dir, "horsh-h5-standalone.html"), os.path.join(deploy_dir, "index.html"))

node = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0\node.exe"
npm_dir = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0\node_modules\npm\bin"

env = os.environ.copy()
env["PATH"] = r"C:\Users\Ms.赵\.workbuddy\binaries\node\versions\22.12.0;" + env.get("PATH", "")
env["NODE_PATH"] = r"C:\Users\Ms.赵\.workbuddy\binaries\node\workspace\node_modules"

# Run surge via node directly
surge_js = r"C:\Users\Ms.赵\.workbuddy\binaries\node\workspace\node_modules\surge\lib\cli.js"
domain = "horsh-bread-2026.surge.sh"

log_path = os.path.join(proj_dir, "surge_log.txt")
with open(log_path, 'w') as log:
    log.write(f"Deploying to {domain}\n")
    log.write(f"Env PATH: {env['PATH'][:200]}\n")
    log.flush()
    
    try:
        proc = subprocess.Popen(
            [node, surge_js, deploy_dir, domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
            cwd=deploy_dir
        )
        
        for line in iter(proc.stdout.readline, ''):
            log.write(line)
            log.flush()
            print(line.strip(), flush=True)
        
        proc.wait(timeout=60)
        log.write(f"\nExit: {proc.returncode}\n")
        
    except subprocess.TimeoutExpired:
        proc.terminate()
        log.write("\nTimeout\n")
    except Exception as e:
        log.write(f"Error: {e}\n")

print(f"\nURL: https://{domain}")
