"""Run all seven scripts, propagating --show/--export/--frames/--fps options."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for p in sorted(root.glob('[0-9][0-9]_*.py')):
 print('\nRunning',p.name,flush=True);subprocess.run([sys.executable,str(p),*sys.argv[1:]],check=True)
subprocess.run([sys.executable,str(root/'verify.py')],check=True)

subprocess.run([sys.executable,str(root/'inventory.py')],check=True)
