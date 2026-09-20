import subprocess, sys
subprocess.run([sys.executable, 'app/ml/train_model.py'])
subprocess.run([sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'])
