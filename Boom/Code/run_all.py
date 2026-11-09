import subprocess
import sys

files = ["geometry.py", "composite.py", "structural_analysis.py"]

for file in files:
    print(f"Running {file}...")
    subprocess.run([sys.executable, file], check=True)

print("All files executed successfully!")
