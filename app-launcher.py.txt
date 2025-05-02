import os
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import subprocess
import time

APP_DIR = '/home/dietpi/app-launcher/apps/'
LAUNCHER_TITLE = 'App Launcher'
ICON_SIZE = (64, 64)

running_apps = {}

def launch_app(app_name, app_path):
    if app_name in running_apps:
        pid = running_apps[app_name]['pid']
        try:
            os.kill(pid, 0)
            window_name = running_apps[app_name]['window_name']
            subprocess.Popen(['xdotool', 'search', '--name', window_name, 'windowactivate'])
            return
        except ProcessLookupError:
            del running_apps[app_name]

    start_script = os.path.join(app_path, 'start.sh')
    if not os.path.isfile(start_script):
        print(f"Kein start.sh in {app_path}")
        return

    process = subprocess.Popen(['bash', start_script])
    time.sleep(2)

    try:
        output = subprocess.check_output(['wmctrl', '-lp']).decode()
        window_id = None
        for line in output.splitlines():
            if str(process.pid) in line:
                parts = line.split()
                window_id = parts[0]
                break

        if window_id:
            win_name = subprocess.check_output(['xdotool', 'getwindowname', window_id]).decode().strip()
        else:
            win_name = app_name

        running_apps[app_name] = {
            'pid': process.pid,
            'window_name': win_name
        }

    except Exception as e:
        print(f"Fehler beim Fenster-Fokus: {e}")

def create_launcher():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title(LAUNCHER_TITLE)
    root.configure(bg='black')

    frame = tk.Frame(root, bg='black')
    frame.pack(expand=True)

    apps = [d for d in os.listdir(APP_DIR) if os.path.isdir(os.path.join(APP_DIR, d))]

    col_count = 5
    row = col = 0

    for app in sorted(apps):
        app_path = os.path.join(APP_DIR, app)
        icon_path = os.path.join(app_path, 'icon.png')

        if os.path.isfile(icon_path):
            try:
                img = Image.open(icon_path).resize(ICON_SIZE)
                icon = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Fehler beim Laden des Icons von {app}: {e}")
                icon = None
        else:
            icon = None

        def on_click(a=app, p=app_path):
            launch_app(a, p)

        btn = tk.Button(frame, text=app, image=icon, compound='top', command=on_click, bg='gray20', fg='white')
        btn.image = icon  # Referenz halten
        btn.grid(row=row, column=col, padx=20, pady=20)

        col += 1
        if col >= col_count:
            col = 0
            row += 1

    root.mainloop()

if __name__ == "__main__":
    create_launcher()
