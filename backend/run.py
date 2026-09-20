import os
import subprocess
import sys

# Train model if not already present
try:
    subprocess.run([sys.executable, 'app/ml/train_model.py'], check=False)
except Exception as e:
    print(f"Notice: {e}")

port = int(os.environ.get("PORT", 8000))
subprocess.run([sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', str(port)])
