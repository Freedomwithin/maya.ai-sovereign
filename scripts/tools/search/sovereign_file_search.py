import tkinter as tk
import customtkinter as ctk
import os
import subprocess
import threading

# Sovereign Palette
P = {
    "bg": "#08080f",
    "surface": "#0d0d1c",
    "border": "#1e1e40",
    "cyan": "#06b6d4",
    "indigo": "#6366f1",
    "red": "#ef4444",
    "text": "#e2e8f0",
    "muted": "#64748b",
    "highlight": "#1a1a2e"
}

# Noise Filter Patterns
NOISE_PATTERNS = [
    "/.cache/", "/Trash/", "/node_modules/", "/.gemini/tmp/", "/.local/share/Trash/",
    "/.venv/", "/__pycache__/", "/.git/"
]

class SovereignFileSearchDesklet(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SOVEREIGN FILES")
        self.geometry("600x180") # Increased base height for controls
        
        self.attributes("-type", "dialog")
        self.attributes("-topmost", True)
        self.configure(fg_color=P["bg"])
        
        sw = self.winfo_screenwidth()
        self.geometry(f"600x180+{(sw-600)//2}+150")

        self.main_frame = ctk.CTkFrame(self, fg_color=P["surface"], border_width=1, border_color=P["border"])
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Header
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 0))
        
        ctk.CTkLabel(header, text="SOVEREIGN FILES", font=("Orbitron", 10, "bold"), text_color=P["cyan"]).pack(side="left", padx=(10, 0))
        
        self.close_btn = ctk.CTkButton(header, text="✕", width=25, height=25, fg_color="transparent", hover_color=P["red"], text_color=P["muted"], font=("Arial", 14, "bold"), command=self.destroy)
        self.close_btn.pack(side="right")
        
        # Search Entry
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="Search your sanctuary...", fg_color=P["bg"], text_color=P["text"], font=("Courier", 12))
        self.entry.pack(fill="x", padx=20, pady=(5, 5))
        self.entry.bind("<Return>", self.start_search_thread)
        
        # Controls Frame
        ctrl_f = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctrl_f.pack(fill="x", padx=20, pady=5)
        
        self.mode_var = tk.StringVar(value="Both")
        ctk.CTkRadioButton(ctrl_f, text="Both", variable=self.mode_var, value="Both", font=("Courier", 10), text_color=P["muted"], width=70).pack(side="left")
        ctk.CTkRadioButton(ctrl_f, text="Files", variable=self.mode_var, value="Files", font=("Courier", 10), text_color=P["muted"], width=70).pack(side="left")
        ctk.CTkRadioButton(ctrl_f, text="Folders", variable=self.mode_var, value="Folders", font=("Courier", 10), text_color=P["muted"], width=80).pack(side="left")
        
        self.deep_var = tk.BooleanVar(value=False)
        self.deep_check = ctk.CTkCheckBox(ctrl_f, text="Deep Hunt (Include Noise)", variable=self.deep_var, font=("Courier", 10), text_color=P["muted"])
        self.deep_check.pack(side="right")

        # Status Label
        self.status_lbl = ctk.CTkLabel(self.main_frame, text="Ready to hunt.", font=("Courier", 9), text_color=P["muted"])
        self.status_lbl.pack(pady=(0, 5))
        
        # Results Listbox
        self.list_frame = ctk.CTkFrame(self.main_frame, fg_color=P["bg"], border_width=1, border_color=P["border"])
        
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", bg=P["bg"])
        self.listbox = tk.Listbox(
            self.list_frame, 
            bg=P["bg"], 
            fg=P["text"], 
            font=("Courier", 11), 
            borderwidth=0, 
            highlightthickness=0,
            selectbackground=P["indigo"],
            selectforeground="white",
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.listbox.yview)
        
        self.listbox.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        self.scrollbar.pack(side="right", fill="y")
        
        self.listbox.bind("<Double-Button-1>", self.open_selected)
        self.listbox.bind("<Return>", self.open_selected)
        self.listbox.bind("<Button-3>", self.show_context_menu) # Right Click

        self.paths = []
        self.bind("<Escape>", lambda e: self.destroy())
        self.after(300, self.grab_the_focus)

    def show_context_menu(self, event):
        index = self.listbox.nearest(event.y)
        if index < 0: return
        
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(index)
        self.listbox.activate(index)
        
        menu = tk.Menu(self, tearoff=0, bg=P["surface"], fg=P["text"], font=("Courier", 10))
        menu.add_command(label=" OPEN ", command=self.open_selected)
        menu.add_command(label=" OPEN LOCATION ", command=self.open_location)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def open_location(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            path = self.paths[index]
            target = path if os.path.isdir(path) else os.path.dirname(path)
            try:
                subprocess.Popen(["xdg-open", target])
                self.destroy()
            except:
                pass

    def grab_the_focus(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.entry.focus_set()
        self.entry.focus_force()

    def start_search_thread(self, event=None):
        query = self.entry.get().strip()
        if not query: return
        
        if query.lower().startswith("find "):
            query = query[5:].strip()
            self.entry.delete(0, "end")
            self.entry.insert(0, query)

        self.status_lbl.configure(text="Searching the lattice...", text_color=P["cyan"])
        self.listbox.delete(0, "end")
        self.list_frame.pack_forget()
            
        threading.Thread(target=self.execute_search, args=(query,), daemon=True).start()

    def execute_search(self, query):
        results = set()
        mode = self.mode_var.get()
        deep = self.deep_var.get()
        workspace = "/home/jonathon/gemini-jules/maya"
        
        # 1. SEARCH WORKSPACE (High Depth, Exclude Noise)
        try:
            find_ws = ["find", workspace, "-maxdepth", "8"]
            if mode == "Folders": find_ws += ["-type", "d"]
            elif mode == "Files": find_ws += ["-type", "f"]
            find_ws += ["-iname", f"*{query}*"]
            
            # Exclude noise at the find level for speed
            if not deep:
                for pattern in NOISE_PATTERNS:
                    clean_pattern = pattern.strip("/")
                    find_ws += ["-not", "-path", f"*/{clean_pattern}/*"]

            output = subprocess.check_output(find_ws, stderr=subprocess.DEVNULL).decode("utf-8")
            for p in output.split("\n"):
                if p.strip(): results.add(p.strip())
        except:
            pass

        # 2. LOCATE FOR SYSTEM (Fast, but can be stale)
        if len(results) < 20:
            try:
                cmd = ["locate", "-i", query]
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8")
                raw_paths = [p for p in output.split("\n") if p.strip()]
                
                for p in raw_paths:
                    if p in results: continue
                    is_dir = os.path.isdir(p)
                    if mode == "Files" and is_dir: continue
                    if mode == "Folders" and not is_dir: continue
                    if not deep and any(pattern in p for pattern in NOISE_PATTERNS): continue
                    results.add(p)
                    if len(results) >= 50: break
            except:
                pass

        # 3. SHALLOW SYSTEM FIND (If still nothing)
        if not results:
            try:
                find_cmd = ["find", os.path.expanduser("~"), "-maxdepth", "4", "-iname", f"*{query}*"]
                if mode == "Folders": find_cmd += ["-type", "d"]
                elif mode == "Files": find_cmd += ["-type", "f"]
                output = subprocess.check_output(find_cmd, stderr=subprocess.DEVNULL).decode("utf-8")
                for p in output.split("\n"):
                    if p.strip(): results.add(p.strip())
            except:
                pass

        # Sort results: Prioritize workspace and then by name length (simpler name first)
        sorted_results = sorted(list(results), key=lambda x: (not x.startswith(workspace), len(os.path.basename(x)), x))
        self.after(0, lambda: self.finalize_results(sorted_results[:40]))

    def finalize_results(self, paths):
        self.paths = paths
        workspace = "/home/jonathon/gemini-jules/maya"
        
        if not paths:
            self.status_lbl.configure(text="The unmanifest remains hidden.", text_color=P["red"])
            self.geometry(f"600x180")
        else:
            self.status_lbl.configure(text=f"Found {len(paths)} signal(s). Double-click to open.", text_color=P["cyan"])
            self.geometry(f"600x550")
            self.list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            for path in paths:
                filename = os.path.basename(path)
                is_dir = os.path.isdir(path)
                prefix = "📁 " if is_dir else "📄 "
                
                # Format the path for display
                if path.startswith(workspace):
                    display_path = os.path.relpath(path, workspace)
                    tag = "[MAYA]"
                else:
                    # Truncate home if possible
                    display_path = path.replace(os.path.expanduser("~"), "~")
                    tag = "[SYS]"
                
                # Truncate middle of long paths
                if len(display_path) > 70:
                    display_path = display_path[:30] + "..." + display_path[-37:]
                
                self.listbox.insert("end", f" {prefix} {tag} {filename}  --  {display_path}")

    def open_selected(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            path = self.paths[index]
            try:
                subprocess.Popen(["xdg-open", path])
                self.destroy()
            except:
                pass

if __name__ == "__main__":
    app = SovereignFileSearchDesklet()
    app.mainloop()
