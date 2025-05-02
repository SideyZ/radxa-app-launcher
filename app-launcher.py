import os
import subprocess
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

APP_DIR = '/home/dietpi/app-launcher/apps/'
LAUNCHER_TITLE = 'App Launcher'
ICON_SIZE = (64, 64)

# Funktion zum Aktivieren eines bereits geöffneten Fensters basierend auf dem Fenstertitel
def activate_existing_window_by_title(window_title):
    try:
        # Finde das Fenster basierend auf dem Titel mit xdotool
        window_ids = subprocess.check_output(['xdotool', 'search', '--name', window_title]).decode().splitlines()
        if window_ids:
            subprocess.Popen(['xdotool', 'windowactivate', window_ids[0]])  # Aktiviert das Fenster mit dem entsprechenden Titel
            return True
    except subprocess.CalledProcessError:
        pass
    return False

# Funktion zum Starten der App
def launch_app(app_name, app_path):
    # Prüfen ob eine window_class.txt vorhanden ist
    window_class_file = os.path.join(app_path, 'window_class.txt')
    if os.path.exists(window_class_file):
        with open(window_class_file, 'r') as f:
            window_class = f.read().strip()
            if activate_existing_window_by_title(app_name):  # Aktiviert Fenster anhand des App-Namens
                print(f"{app_name} ist bereits aktiv, aktiviere Fenster...")
                return  # Wenn die App bereits aktiv ist, nichts weiter tun

    # Fallback: Wenn keine window_class.txt vorhanden ist, starte die App normal
    start_script = os.path.join(app_path, 'start.sh')
    if not os.path.isfile(start_script):
        print(f"Kein start.sh in {app_path}")
        return

    # Starte die App in einem neuen xterm-Fenster mit dem Ordnernamen als Fenstertitel
    subprocess.Popen(['xterm', '-T', app_name, '-e', 'bash', start_script])
    print(f"{app_name} wurde gestartet.")

# Erstelle den Launcher
def create_launcher():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title(LAUNCHER_TITLE)
    root.configure(bg='black')

    frame = tk.Frame(root, bg='black')
    frame.pack(expand=True)

    # Hole die Liste der Apps aus dem Verzeichnis
    apps = [d for d in os.listdir(APP_DIR) if os.path.isdir(os.path.join(APP_DIR, d))]

    col_count = 5
    row = col = 0

    for app in sorted(apps):
        app_path = os.path.join(APP_DIR, app)
        icon_path = os.path.join(app_path, 'icon.png')

        # Lade das App-Icon, falls vorhanden
        if os.path.isfile(icon_path):
            try:
                img = Image.open(icon_path).resize(ICON_SIZE)
                icon = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Fehler beim Laden des Icons von {app}: {e}")
                icon = None
        else:
            icon = None

        # Callback-Funktion für den Button, der die App startet
        def on_click(a=app, p=app_path):
            launch_app(a, p)

        # Erstelle den Button für jede App
        btn = tk.Button(frame, text=app, image=icon, compound='top', command=on_click, bg='gray20', fg='white')
        btn.image = icon  # Referenz behalten
        btn.grid(row=row, column=col, padx=20, pady=20)

        col += 1
        if col >= col_count:
            col = 0
            row += 1

    root.mainloop()

# Hauptfunktion, die den Launcher startet
if __name__ == "__main__":
    create_launcher()
