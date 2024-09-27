import sys
import subprocess
#subprocess.check_call([sys.executable,"--version"])
subprocess.check_call([sys.executable,"-m","ensurepip","--upgrade"])
# implement pip as a subprocess:$
subprocess.check_call([sys.executable, 'curl', 'https://bootstrap.pypa.io/get-pip.py', '-o','get-pip.py'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'simpleaudio'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade Pillow'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ttkbootstrap'])