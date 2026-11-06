# ==================================================
# 🌑 SHADOW — Desktop App (chat look)
# Run with Launch_Shadow_App.bat
# ==================================================

import threading
import customtkinter as ctk
from tkinter import filedialog

from security import detect_injection, read_file_safe
from shadow_core import ask_team, ollama_online

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

BG, USER_BUBBLE, AI_BUBBLE, SYS_TEXT = "#0f1117", "#1f7a4d", "#232733", "#8a8fa3"
READY = "Enter = send, Shift+Enter = new line"

history = []
file_context = {"text": "", "name": ""}


def add_bubble(text, who="ai"):
    row = ctk.CTkFrame(chat_frame, fg_color="transparent")
    row.pack(fill="x", padx=10, pady=4)
    if who == "system":
        ctk.CTkLabel(row, text=text, text_color=SYS_TEXT,
                     font=("Segoe UI", 11, "italic")).pack(anchor="center")
    else:
        is_user = who == "user"
        ctk.CTkLabel(row, text=text, wraplength=560, justify="left", anchor="w",
                     font=("Segoe UI", 13),
                     fg_color=USER_BUBBLE if is_user else AI_BUBBLE,
                     text_color="white", corner_radius=14, padx=14, pady=10
                     ).pack(anchor="e" if is_user else "w",
                            padx=(80, 0) if is_user else (0, 80))
    app.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)


def set_busy(busy):
    send_btn.configure(state="disabled" if busy else "normal",
                       text="⏳ ..." if busy else "🚀 Send")


def worker(user_text):
    ui = lambda fn, *a, **k: app.after(0, lambda: fn(*a, **k))
    answer = ask_team(user_text, history=list(history),
                      file_context=file_context["text"],
                      on_status=lambda s: ui(status.configure, text=s))
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": answer})
    ui(add_bubble, f"🐬 Dola\n{answer}", "ai")
    ui(status.configure, text=READY)
    ui(set_busy, False)


def send(event=None):
    text = input_box.get("1.0", "end").strip()
    if not text or send_btn.cget("state") == "disabled":
        return "break"
    input_box.delete("1.0", "end")
    if detect_injection(text):
        add_bubble("⚠️ Suspicious input — processed with protection", "system")
    add_bubble(text, "user")
    set_busy(True)
    threading.Thread(target=worker, args=(text,), daemon=True).start()
    return "break"


def attach_file():
    path = filedialog.askopenfilename()
    if path:
        file_context["text"] = read_file_safe(path)
        file_context["name"] = path.split("/")[-1].split("\\")[-1]
        add_bubble(f"📎 Attached: {file_context['name']}", "system")


# ─── Window ───
app = ctk.CTk(fg_color=BG)
app.title("🌑 SHADOW — Personal AI")
app.geometry("900x700")

ctk.CTkLabel(app, text="🌑 SHADOW", font=("Segoe UI", 22, "bold")).pack(pady=(14, 0))
ctk.CTkLabel(app, text="Your personal AI team", text_color=SYS_TEXT,
             font=("Segoe UI", 12)).pack(pady=(0, 8))

chat_frame = ctk.CTkScrollableFrame(app, fg_color=BG)
chat_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

bar = ctk.CTkFrame(app, fg_color="transparent")
bar.pack(fill="x", padx=12, pady=(0, 6))

ctk.CTkButton(bar, text="📎", width=50, height=60, corner_radius=12,
              command=attach_file).pack(side="left", padx=(0, 8))
input_box = ctk.CTkTextbox(bar, height=60, wrap="word", font=("Segoe UI", 13), corner_radius=12)
input_box.pack(side="left", fill="x", expand=True, padx=(0, 8))
input_box.bind("<Return>", send)
input_box.bind("<Shift-Return>", lambda e: None)

send_btn = ctk.CTkButton(bar, text="🚀 Send", width=110, height=60, corner_radius=12,
                         font=("Segoe UI", 14, "bold"), command=send)
send_btn.pack(side="right")

status = ctk.CTkLabel(app, text=READY, text_color=SYS_TEXT, font=("Segoe UI", 10))
status.pack(pady=(0, 6))

if ollama_online():
    add_bubble("🐬 Dola\nHi! SHADOW is ready. Ask me anything — I check with the team and pick the best answer.", "ai")
else:
    add_bubble("⚠️ Ollama is not running. Open Ollama (or run: ollama serve), then send your message again.", "system")

input_box.focus()
app.mainloop()