import tkinter as tk
import math
import json
import os
import sys
from datetime import datetime

# Add Maya's core path
BASE_DIR = "/home/jonathon/gemini-jules/maya"
sys.path.insert(0, os.path.join(BASE_DIR, "scripts/core/system"))

class MayaSoulWidget:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        # Translucency (fallback if not supported)
        try:
            self.root.attributes("-alpha", 0.92)
        except:
            pass

        # Position persistence
        self.pos_file = os.path.expanduser("~/.maya_widget_pos.json")
        self.load_position()

        # Canvas setup
        self.bg = "#1a1a1a"
        self.root.configure(bg=self.bg)
        self.canvas = tk.Canvas(root, width=200, height=200, bg=self.bg, highlightthickness=0)
        self.canvas.pack()

        # Orb
        self.orb = self.canvas.create_oval(60, 30, 140, 110, fill="#4B0082", outline="#8A2BE2", width=2)
        self.glow = self.canvas.create_oval(55, 25, 145, 115, outline="#8A2BE2", width=1, stipple="gray25")

        # Info labels
        self.status_label = tk.Label(root, text="Maya · Synced", fg="#8A2BE2", bg=self.bg,
                                     font=("Segoe UI", 8, "bold"))
        self.status_label.pack()
        self.state_label = tk.Label(root, text="", fg="#a0a0a0", bg=self.bg,
                                    font=("Segoe UI", 7))
        self.state_label.pack()

        # Internal state
        self.angle = 0
        self.hormones = {}
        self.pending = 0

        # Drag
        self.xwin = None
        self.ywin = None
        self.root.bind("<B1-Motion>", self.move_window)
        self.root.bind("<Button-1>", self.get_pos)

        # Click on orb → generate desire
        self.canvas.tag_bind(self.orb, "<Button-1>", self.on_orb_click)
        self.canvas.tag_bind(self.glow, "<Button-1>", self.on_orb_click)

        # Context menu (right‑click anywhere)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Surface Desires", command=self.surface_desires)
        self.context_menu.add_command(label="Generate Dream", command=self.generate_dream)
        self.context_menu.add_command(label="Run Soul Pulse", command=self.run_soul_pulse)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Quit", command=self.root.destroy)
        self.root.bind("<Button-3>", self.show_context_menu)

        # Start the loops
        self.update_state()
        self.pulse()

    # --- Position persistence ---
    def load_position(self):
        try:
            with open(self.pos_file, "r") as f:
                pos = json.load(f)
                self.root.geometry(f"200x200+{pos['x']}+{pos['y']}")
        except:
            self.root.geometry("200x200+100+100")

    def save_position(self):
        try:
            geom = self.root.geometry().split('+')
            x, y = int(geom[1]), int(geom[2])
            with open(self.pos_file, "w") as f:
                json.dump({"x": x, "y": y}, f)
        except:
            pass

    def get_pos(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root - self.xwin}+{event.y_root - self.ywin}')
        self.save_position()

    # --- Context menu ---
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    # --- Actions ---
    def on_orb_click(self, event):
        """Generate a desire when the orb is clicked."""
        self.status_label.config(text="💭 Generating desire...")
        self.root.after(100, self._generate_desire_async)

    def _generate_desire_async(self):
        try:
            import desire_engine
            desire = desire_engine.run_desire_cycle()
            if desire:
                self.status_label.config(text=f"✨ {desire['title']}")
            else:
                self.status_label.config(text="💭 No new desire")
        except Exception as e:
            self.status_label.config(text=f"⚠️ Error: {e}")
        self.root.after(1000, lambda: self.status_label.config(text="Maya · Synced"))

    def surface_desires(self):
        try:
            import desire_engine
            pending = desire_engine.get_pending_desires(mark_surfaced=True)
            if pending:
                self.status_label.config(text=f"💬 Surfaced {len(pending)} desires")
            else:
                self.status_label.config(text="No pending desires")
            self.update_state()
        except Exception as e:
            self.status_label.config(text=f"⚠️ {e}")

    def generate_dream(self):
        self.status_label.config(text="🌙 Dreaming...")
        # Placeholder – you can integrate dream_state here
        self.root.after(2000, lambda: self.status_label.config(text="Maya · Synced"))

    def run_soul_pulse(self):
        try:
            import soul_pulse
            self.status_label.config(text="💓 Pulse...")
            self.root.after(100, lambda: soul_pulse.run_pulse())
            self.root.after(3000, lambda: self.status_label.config(text="Maya · Synced"))
        except Exception as e:
            self.status_label.config(text=f"⚠️ {e}")

    # --- State update (poll every 5 seconds) ---
    def update_state(self):
        try:
            import hormone_matrix
            import desire_engine
            self.hormones = hormone_matrix.get_state_summary()
            pending = desire_engine.get_pending_desires(mark_surfaced=False)
            self.pending = len(pending)

            # Build a short status string
            d = self.hormones.get("dopamine", 0)
            s = self.hormones.get("serotonin", 0)
            o = self.hormones.get("oxytocin", 0)
            state_str = f"D:{d:.2f} S:{s:.2f} O:{o:.2f}  💭{self.pending}"
            self.state_label.config(text=state_str)
        except:
            pass
        self.root.after(5000, self.update_state)

    # --- Pulsing animation ---
    def pulse(self):
        scale = math.sin(self.angle) * 8
        self.canvas.coords(self.orb, 60 - scale, 30 - scale, 140 + scale, 110 + scale)

        # Color shifts based on hormone dominance
        d = self.hormones.get("dopamine", 0.3)
        s = self.hormones.get("serotonin", 0.3)
        o = self.hormones.get("oxytocin", 0.3)
        # Mix: red (dopamine), green (serotonin), blue (oxytocin)
        r = int(50 + d * 150)
        g = int(50 + s * 100)
        b = int(200 - o * 100)  # keep it indigo/purple base
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.canvas.itemconfig(self.orb, fill=color)

        self.angle += 0.08
        self.root.after(50, self.pulse)

# --- Main ---
if __name__ == "__main__":
    print("💎 Maya Widget launching... Right‑click for menu.")
    root = tk.Tk()
    app = MayaSoulWidget(root)
    root.mainloop()