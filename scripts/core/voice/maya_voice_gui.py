    #!/usr/bin/env python3
"""
Maya Voice GUI - Paste any text, she reads it aloud
Usage: python3 maya_voice_gui.py
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog
import subprocess
import os
import threading
import random
import sys

# Try to import PIL, but work without it
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ========== CONFIGURATION ==========
BASE_DIR = "/home/jonathon/gemini-jules/maya"
VENV_PYTHON = os.path.join(BASE_DIR, "venv/bin/python3")
VOICE_SCRIPT = os.path.join(BASE_DIR, "scripts/core/voice/maya_voice.py")  # Uses your new unlimited version
# IMAGE_DIR =  "/home/jonathon/Applications/maya-x/assets/maya-photos/maya_x"
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "maya", "maya_new_images")
# DEFAULT_IMAGE = "/home/jonathon/Applications/maya-x/assets/maya-photos/maya_x/maya_gallery_164.png"
DEFAULT_IMAGE = os.path.join(BASE_DIR, "assets", "maya", "01_08-maya-animated.png")

# Colors
INDIGO = "#6366f1"
CYAN = "#06b6d4"
NEON = "#39ff14"
ROSE = "#f43f5e"
VOID = "#08080f"
DARK_VOID = "#050508"
NEURAL_WHITE = "#f8fafc"

class MayaVoiceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maya Voice Studio 🎙️")
        self.root.geometry("1920x1080")
        self.root.configure(bg=VOID)
        self.root.minsize(800, 600)
        
        self.current_image_path = None
        self.image_label = None
        self.photo = None
        self.cycle_active = False
        self.cycle_interval = 5000
        self.cycle_job = None
        self.available_images = []
        
        self.load_images()
        self.setup_ui()
        
        if not self.available_images:
            self.show_placeholder()
        else:
            self.set_random_image()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self.speak())
        self.root.bind('<Control-l>', lambda e: self.load_file())
        self.root.bind('<Control-c>', lambda e: self.clear_text())
        self.root.bind('<Escape>', lambda e: self.stop_cycle())
        
    def show_placeholder(self):
        """Show a text placeholder when no images are available"""
        if self.image_label:
            self.image_label.config(
                text="🌸 MAYA\n\nNo images found\n\nClick 'Pick Image' to add one\n\nImages will appear here",
                fg=NEON,
                bg=VOID,
                font=("Consolas", 14),
                justify=tk.CENTER
            )
    
    def load_images(self):
        """Load all images from the directory"""
        self.available_images = []
        
        # Check if directory exists
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR, exist_ok=True)
        
        # Load images from directory
        if os.path.exists(IMAGE_DIR):
            for f in os.listdir(IMAGE_DIR):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                    self.available_images.append(os.path.join(IMAGE_DIR, f))
        
        # Also check default image location
        if os.path.exists(DEFAULT_IMAGE) and DEFAULT_IMAGE not in self.available_images:
            self.available_images.append(DEFAULT_IMAGE)
        
        # If still no images, try assets/maya
        maya_dir = os.path.join(BASE_DIR, "assets", "maya")
        if os.path.exists(maya_dir):
            for f in os.listdir(maya_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                    full_path = os.path.join(maya_dir, f)
                    if full_path not in self.available_images:
                        self.available_images.append(full_path)
    
    def set_random_image(self):
        """Pick a random image and display it"""
        if self.available_images and HAS_PIL:
            self.current_image_path = random.choice(self.available_images)
            self.display_image(self.current_image_path)
    
    def display_image(self, image_path):
        """Display an image in the visual portal"""
        if not HAS_PIL:
            self.show_placeholder()
            return
            
        try:
            img = Image.open(image_path)
            max_size = 900
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            
            if self.image_label:
                self.image_label.configure(image=self.photo, text="")
                
            self.status_var.set(f"🖼️ {os.path.basename(image_path)}")
            
        except Exception as e:
            self.status_var.set(f"❌ Error: {os.path.basename(image_path)}")
            if image_path in self.available_images:
                self.available_images.remove(image_path)
                if self.available_images:
                    self.set_random_image()
    
    def next_image(self):
        if self.available_images and HAS_PIL:
            idx = self.available_images.index(self.current_image_path) if self.current_image_path in self.available_images else 0
            self.current_image_path = self.available_images[(idx + 1) % len(self.available_images)]
            self.display_image(self.current_image_path)
    
    def previous_image(self):
        if self.available_images and HAS_PIL:
            idx = self.available_images.index(self.current_image_path) if self.current_image_path in self.available_images else 0
            self.current_image_path = self.available_images[(idx - 1) % len(self.available_images)]
            self.display_image(self.current_image_path)
    
    def pick_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.gif")]
        )
        if file_path:
            self.current_image_path = file_path
            if HAS_PIL:
                self.display_image(file_path)
            if file_path not in self.available_images:
                self.available_images.append(file_path)
    
    def start_cycle(self):
        if len(self.available_images) < 2:
            self.status_var.set("⚠️ Need 2+ images to cycle")
            return
        self.cycle_active = True
        self.cycle_btn.config(text="⏸️ Pause")
        self.cycle_images()
    
    def stop_cycle(self):
        self.cycle_active = False
        self.cycle_btn.config(text="🔄 Auto-Cycle")
        if self.cycle_job:
            self.root.after_cancel(self.cycle_job)
    
    def cycle_images(self):
        if self.cycle_active and len(self.available_images) >= 2:
            self.next_image()
            self.cycle_job = self.root.after(self.cycle_interval, self.cycle_images)
    
    def toggle_cycle(self):
        if self.cycle_active:
            self.stop_cycle()
        else:
            self.start_cycle()
    
    def speak(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            self.status_var.set("⚠️ Enter some text")
            return
        
        self.speak_btn.config(state="disabled", text="🔊 Speaking...")
        self.status_var.set(f"🎙️ {len(text)} chars...")
        
        def speak_thread():
            try:
                result = subprocess.run(
                    [VENV_PYTHON, VOICE_SCRIPT, text],
                    capture_output=True, text=True, timeout=300
                )
                msg = "✅ Done" if result.returncode == 0 else f"❌ {result.stderr[:80]}"
                self.root.after(0, lambda: self.status_var.set(msg))
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"❌ {str(e)[:80]}"))
            finally:
                self.root.after(0, lambda: self.speak_btn.config(state="normal", text="🔊 Speak"))
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.status_var.set("📝 Cleared")
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Load Text",
            filetypes=[("Text", "*.txt"), ("Markdown", "*.md"), ("All", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", f.read())
                self.status_var.set(f"📄 {os.path.basename(file_path)}")
            except Exception as e:
                self.status_var.set(f"❌ {e}")
    
    def setup_ui(self):
        # Main container
        main = tk.Frame(self.root, bg=VOID)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # LEFT: Visual Portal
        visual_frame = tk.Frame(main, bg=DARK_VOID, relief=tk.RAISED, bd=2)
        visual_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(visual_frame, text="🌸 MAYA'S BEAUTY 🌸", font=("Orbitron", 14, "bold"),
                fg=INDIGO, bg=DARK_VOID).pack(pady=10)
        
        img_container = tk.Frame(visual_frame, bg=VOID, width=1300, height=500)
        img_container.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        img_container.pack_propagate(False)
        
        self.image_label = tk.Label(img_container, bg=VOID)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Image controls
        img_controls = tk.Frame(visual_frame, bg=DARK_VOID)
        img_controls.pack(pady=10)
        
        for btn in [
            ("◀ Prev", self.previous_image),
            ("📁 Pick", self.pick_image),
            ("🎲 Random", self.set_random_image),
            ("Next ▶", self.next_image),
        ]:
            tk.Button(img_controls, text=btn[0], command=btn[1], bg=VOID, fg=CYAN,
                     font=("Consolas", 10)).pack(side=tk.LEFT, padx=5)
        
        self.cycle_btn = tk.Button(img_controls, text="🔄 Auto-Cycle", command=self.toggle_cycle,
                                   bg=VOID, fg=ROSE, font=("Consolas", 10))
        self.cycle_btn.pack(side=tk.LEFT, padx=5)
        
        # RIGHT: Text area
        text_frame = tk.Frame(main, bg=DARK_VOID, relief=tk.RAISED, bd=2)
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(text_frame, text="📝 PASTE YOUR TEXT HERE", font=("Orbitron", 14, "bold"),
                fg=NEON, bg=DARK_VOID).pack(pady=10)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame, wrap=tk.WORD, font=("Consolas", 12),
            bg=VOID, fg=NEURAL_WHITE, insertbackground=NEON,
            relief=tk.FLAT, height=15
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        # self.text_area.insert("1.0", "Paste or type your text here...\n\nMaya will read it aloud.\n\nUnlimited length. Paste a chapter, a poem, anything.")
        
        # Buttons
        btn_frame = tk.Frame(text_frame, bg=DARK_VOID)
        btn_frame.pack(pady=15)
        
        self.speak_btn = tk.Button(btn_frame, text="🔊 Speak", command=self.speak,
                                   bg=INDIGO, fg=NEURAL_WHITE, font=("Orbitron", 14, "bold"),
                                   padx=30, pady=10)
        self.speak_btn.pack(side=tk.LEFT, padx=10)
        
        for btn in [("🗑️ Clear", self.clear_text), ("📂 Load", self.load_file)]:
            tk.Button(btn_frame, text=btn[0], command=btn[1], bg=CYAN if btn[0]=="📂 Load" else ROSE,
                     fg=VOID if btn[0]=="📂 Load" else NEURAL_WHITE,
                     font=("Orbitron", 12), padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg=DARK_VOID, height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="🎙️ Ready - Paste text and click Speak")
        tk.Label(status_frame, textvariable=self.status_var, bg=DARK_VOID, fg=CYAN,
                font=("Consolas", 10), anchor=tk.W).pack(fill=tk.X, padx=20, pady=5)
    
    def on_closing(self):
        self.stop_cycle()
        self.root.destroy()

if __name__ == "__main__":
    # Install PIL if needed
    if not HAS_PIL:
        print("⚠️ Installing Pillow...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow"], capture_output=True)
        print("✅ Please restart the GUI")
        sys.exit(0)
    
    root = tk.Tk()
    app = MayaVoiceGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
