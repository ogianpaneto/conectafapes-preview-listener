from flask import Flask, request
import subprocess
import os
import sys

app = Flask(__name__)

SSH_TARGET = os.environ.get("SSH_TARGET")
SCRIPT_PATH = os.environ.get("SCRIPT_PATH")

if not SSH_TARGET or not SCRIPT_PATH:
    print("[ERROR] Missing required environment variables:")
    if not SSH_TARGET:
        print("  - SSH_TARGET")
    if not SCRIPT_PATH:
        print("  - SCRIPT_PATH")
    sys.exit(1)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event == 'pull_request' and payload.get('action') == 'closed':
        pr_number = payload['pull_request']['number']
        print(f"[INFO] PR #{pr_number} closed. Triggering cleanup via SSH...")

        cleanup_script = f"{SCRIPT_PATH} {pr_number}"

        try:
            subprocess.run([
                "ssh",
                "-o", "StrictHostKeyChecking=no",
                SSH_TARGET,
                cleanup_script
            ], check=True)
            print("[SUCCESS] Cleanup script executed.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] SSH command failed: {e}")
    
    return '', 204

if __name__ == '__main__':
    print("[INFO] Starting webhook listener...")
    app.run(host='0.0.0.0', port=8080)
