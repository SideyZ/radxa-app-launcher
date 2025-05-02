import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

APP_DIR = "/home/dietpi/app-launcher/apps"

class AppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App Launcher")
        self.configure(bg="black")

        # Vollbild aktivieren
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())  # ESC zum Beenden

        self.icon_size = (64, 64)
        self.default_icon = self.create_default_icon()

        self.load_apps()

    def create_default_icon(self):
        """Erzeugt ein graues Platzhalterbild."""
        img = Image.new("RGB", self.icon_size, color="gray")
        return ImageTk.PhotoImage(img)

    def load_apps(self):
        row = 0
        column = 0

        for app_name in sorted(os.listdir(APP_DIR)):
            app_path = os.path.join(APP_DIR, app_name)
            start_script = os.path.join(app_path, "start.sh")

            if not os.path.isfile(start_script) or not os.access(start_script, os.R_OK):
                continue  # Startskript muss vorhanden und lesbar sein

            icon = self.default_icon
            icon_path = os.path.join(app_path, "icon.png")
            if os.path.isfile(icon_path):
                try:
                    img = Image.open(icon_path)
                    img = img.resize(self.icon_size, Image.ANTIALIAS)
                    icon = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"[WARNUNG] Fehler beim Laden von {icon_path}: {e}")

            btn = tk.Button(self, image=icon, command=lambda p=start_script: self.launch_app(p), bg="black", borderwidth=0)
            btn.image = icon
            btn.grid(row=row, column=column, padx=10, pady=10)

            lbl = tk.Label(self, text=app_name, fg="white", bg="black")
            lbl.grid(row=row + 1, column=column)

            column += 1
            if column >= 4:
                column = 0
                row += 2

    def launch_app(self, script_path):
        """Startet die App im Hintergrund, ohne den Launcher zu blockieren."""
        try:
            subprocess.Popen(["bash", script_path])  # App im Hintergrund starten
        except Exception as e:
            messagebox.showerror("Fehler", f"Kann App nicht starten:\n{e}")

if __name__ == "__main__":
    launcher = AppLauncher()
    launcher.mainloop()
