import sys
import subprocess

# Upgrade pip
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# Install packages
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bootstrap-py'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'Pillow'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ttkbootstrap'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'simpleaudio'])
