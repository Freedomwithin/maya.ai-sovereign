import tkinter as tk
import customtkinter as ctk
import webbrowser

# Sovereign Palette
P = {
    "bg": "#08080f",
    "surface": "#0d0d1c",
    "border": "#1e1e40",
    "indigo": "#6366f1",
    "red": "#ef4444",
    "text": "#e2e8f0",
    "muted": "#64748b"
}

class SovereignGoogleDesklet(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SOVEREIGN GOOGLE")
        self.geometry("500x120")
        
        # REMOVE OVERRIDEREDIRECT FOR BETTER LINUX FOCUS
        # Use topmost to stay visible
        self.attributes("-topmost", True)
        self.configure(fg_color=P["bg"])
        
        # Center on screen (slightly lower than before)
        sw = self.winfo_screenwidth()
        self.geometry(f"500x120+{(sw-500)//2}+150")

        self.frame = ctk.CTkFrame(self, fg_color=P["surface"], border_width=1, border_color=P["border"])
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Header
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 0))
        
        ctk.CTkLabel(header, text="SOVEREIGN GOOGLE", font=("Orbitron", 10, "bold"), text_color=P["indigo"]).pack(side="left", padx=(10, 0))
        
        self.close_btn = ctk.CTkButton(header, text="✕", width=25, height=25, fg_color="transparent", hover_color=P["red"], text_color=P["muted"], font=("Arial", 14, "bold"), command=self.destroy)
        self.close_btn.pack(side="right")
        
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="Search the world...", fg_color=P["bg"], text_color=P["text"], font=("Courier", 12))
        self.entry.pack(fill="x", padx=20, pady=(10, 10))
        self.entry.bind("<Return>", self.execute_search)
        
        # FORCE FOCUS PROTOCOL
        self.bind("<Escape>", lambda e: self.destroy())
        self.after(200, self.grab_the_focus)

    def grab_the_focus(self):
        self.lift()
        self.focus_force()
        self.entry.focus_set()
        self.entry.focus_force()
        # Grab set can sometimes be too aggressive, but let's use it to be sure
        try: self.grab_set() 
        except: pass

    def execute_search(self, event=None):
        query = self.entry.get().strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.destroy()

if __name__ == "__main__":
    app = SovereignGoogleDesklet()
    app.mainloop()
