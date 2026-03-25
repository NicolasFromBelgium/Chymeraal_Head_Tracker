"""GUI simple et propre avec flèche 3D (pitch + yaw) sur grille 3D."""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import math

try:
    import tkinter as tk
except ImportError:
    raise ImportError(
        "Tkinter is not available.\nSur Debian/Ubuntu : sudo apt install python3-tk tk"
    ) from None

from .quest_tracker import QuestTracker
from .orientation import Quaternion


class HeadTrackerGUI:
    def __init__(self, tracker: QuestTracker):
        self.tracker = tracker
        self.root = tk.Tk()
        self.root.title("Chymeraal Head Tracker - Quest 3")

        # Icône barre des tâches
        icon_path = Path(__file__).parent.parent.parent / "logo_notext_white.png"
        if icon_path.exists():
            self.icon_img = tk.PhotoImage(file=str(icon_path))
            self.root.iconphoto(True, self.icon_img)

        self.root.geometry("720x680")
        self.root.resizable(True, True)

        self.pitch_var = tk.DoubleVar(value=0.0)
        self.yaw_var = tk.DoubleVar(value=0.0)
        self.roll_var = tk.DoubleVar(value=0.0)
        self.status_var = tk.StringVar(value="Disconnected - Cliquez sur Simulate pour tester")

        self._create_widgets()
        self._schedule_update()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header, text="Quest 3 Head Tracking", font=("Helvetica", 18, "bold")).pack(
            side=tk.LEFT
        )

        logo_path = Path(__file__).parent.parent.parent / "Chymeraal_OS_release_logo.png"
        if logo_path.exists():
            self.logo_img = tk.PhotoImage(file=str(logo_path)).subsample(2)
            ttk.Label(header, image=self.logo_img).pack(side=tk.RIGHT)

        ttk.Label(main_frame, textvariable=self.status_var, foreground="#00cc00").pack(pady=5)

        # Valeurs numériques
        values_frame = ttk.LabelFrame(main_frame, text="Orientation (degrés)", padding=12)
        values_frame.pack(fill=tk.X, pady=10)

        ttk.Label(values_frame, text="Pitch:").grid(row=0, column=0, sticky="w", padx=15, pady=6)
        ttk.Label(values_frame, textvariable=self.pitch_var, font=("Helvetica", 14, "bold")).grid(
            row=0, column=1, sticky="w", padx=15
        )

        ttk.Label(values_frame, text="Yaw:").grid(row=1, column=0, sticky="w", padx=15, pady=6)
        ttk.Label(values_frame, textvariable=self.yaw_var, font=("Helvetica", 14, "bold")).grid(
            row=1, column=1, sticky="w", padx=15
        )

        ttk.Label(values_frame, text="Roll:").grid(row=2, column=0, sticky="w", padx=15, pady=6)
        ttk.Label(values_frame, textvariable=self.roll_var, font=("Helvetica", 14, "bold")).grid(
            row=2, column=1, sticky="w", padx=15
        )

        # === Zone 3D : Grille + Flèche ===
        self.canvas = tk.Canvas(
            main_frame,
            width=500,
            height=500,
            bg="#0a0a0a",
            highlightthickness=2,
            highlightbackground="#444",
        )
        self.canvas.pack(pady=15)

        # Boutons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Simulate Random Data", command=self._simulate_data).pack(
            side=tk.LEFT, padx=6
        )
        ttk.Button(btn_frame, text="Select Device", command=self._select_device).pack(
            side=tk.LEFT, padx=6
        )
        ttk.Button(btn_frame, text="Reset", command=self._reset).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Quit", command=self.root.quit).pack(side=tk.LEFT, padx=6)

    def _schedule_update(self):
        orient = self.tracker.get_orientation()
        if orient:
            self.pitch_var.set(round(orient.pitch, 2))
            self.yaw_var.set(round(orient.yaw, 2))
            self.roll_var.set(round(orient.roll, 2))
            self.status_var.set("✅ Connected - Receiving live data")
            self._draw_3d_arrow(orient.pitch, orient.yaw)
        else:
            self.status_var.set("Disconnected - Cliquez sur Simulate pour tester")

        self.root.after(50, self._schedule_update)

    def _draw_3d_arrow(self, pitch: float, yaw: float):
        """Dessine une grille 3D + une flèche (cylindre + cône) qui pointe selon pitch et yaw."""
        self.canvas.delete("all")
        cx, cy = 250, 250
        size = 220

        # Grille 3D fine (perspective simple)
        for i in range(-4, 5):
            offset = i * 45
            # Lignes horizontales
            self.canvas.create_line(
                cx - size, cy + offset, cx + size, cy + offset, fill="#333333", width=1
            )
            # Lignes verticales avec légère perspective
            self.canvas.create_line(
                cx + offset, cy - size, cx + offset * 0.6, cy + size, fill="#333333", width=1
            )

        # Flèche 3D : direction selon pitch et yaw
        # Conversion en coordonnées écran (inversion Y car canvas a Y vers le bas)
        yaw_rad = math.radians(yaw)
        pitch_rad = math.radians(pitch)

        length = 160
        dx = length * math.sin(yaw_rad) * math.cos(pitch_rad)
        dy = length * math.sin(pitch_rad)  # négatif = vers le haut de l'écran

        end_x = cx + dx
        end_y = cy - dy

        # Cylindre (corps de la flèche)
        self.canvas.create_line(cx, cy, end_x, end_y, fill="#00ffaa", width=8, capstyle=tk.ROUND)

        # Cônes à l'avant (pointe)
        cone_length = 25
        cone_dx = cone_length * math.sin(yaw_rad) * math.cos(pitch_rad)
        cone_dy = cone_length * math.sin(pitch_rad)

        tip_x = end_x + cone_dx
        tip_y = end_y - cone_dy

        # Deux lignes pour simuler le cône
        self.canvas.create_line(end_x, end_y, tip_x, tip_y, fill="#00ffaa", width=12)
        self.canvas.create_line(end_x - 8, end_y - 5, tip_x, tip_y, fill="#00ffaa", width=6)
        self.canvas.create_line(end_x + 8, end_y + 5, tip_x, tip_y, fill="#00ffaa", width=6)

        # Petite sphère au centre (point de pivot)
        self.canvas.create_oval(
            cx - 8, cy - 8, cx + 8, cy + 8, fill="#ff4444", outline="#ffffff", width=2
        )

        # Légende
        self.canvas.create_text(
            250,
            30,
            text=f"Pitch: {pitch:+.1f}°   Yaw: {yaw:+.1f}°",
            fill="#ffffff",
            font=("Helvetica", 11, "bold"),
        )

    def _simulate_data(self):
        import random

        q = Quaternion(
            x=random.uniform(-0.7, 0.7),
            y=random.uniform(-0.7, 0.7),
            z=random.uniform(-0.4, 0.4),
            w=random.uniform(0.5, 1.0),
        )
        self.tracker.update_orientation(q)

    def _select_device(self):
        messagebox.showinfo(
            "Select Device", "Quest 3 sélectionné\n\nUDP prêt pour la connexion réelle."
        )

    def _reset(self):
        self.tracker._current_orientation = None
        self.tracker._connected = False

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    tracker = QuestTracker()
    gui = HeadTrackerGUI(tracker)
    gui.run()
