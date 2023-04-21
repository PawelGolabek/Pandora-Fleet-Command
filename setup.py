import sys
import subprocess

# implement pip as a subprocess:$ 
subprocess.check_call([sys.executable, 'curl', '-sSL', 'https://bootstrap.pypa.io/get-pip.py', '-o','get-pip.py'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade Pillow'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ttkbootstrap'])