import json
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

from utils import FAQChatbotEngine


class FAQChatbotGUI:
    """A modern desktop GUI for the FAQ chatbot using Tkinter."""

    def __init__(self, root: tk.Tk, faq_path: str):
        self.root = root
        self.root.title("CodeAlpha AI FAQ Chatbot")
        self.root.geometry("950x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#0f172a")

        self.engine = FAQChatbotEngine(faq_path=faq_path)
        self._build_ui()

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = tk.Frame(self.root, bg="#111827", padx=20, pady=16)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(
            header,
            text="AI FAQ Assistant",
            font=("Segoe UI", 20, "bold"),
            fg="#f8fafc",
            bg="#111827",
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Ask anything about Python, AI, ML, data science, programming, and internships.",
            font=("Segoe UI", 10),
            fg="#cbd5e1",
            bg="#111827",
        ).pack(anchor="w", pady=(4, 0))

        chat_frame = tk.Frame(self.root, bg="#111827")
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 12))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)

        self.chat_canvas = tk.Canvas(chat_frame, bg="#111827", highlightthickness=0)
        self.chat_canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_window = tk.Frame(self.chat_canvas, bg="#111827")
        self.chat_canvas.create_window((0, 0), window=self.chat_window, anchor="nw")
        self.chat_window.bind("<Configure>", self._on_frame_configure)

        bottom_frame = tk.Frame(self.root, bg="#111827", padx=16, pady=12)
        bottom_frame.grid(row=2, column=0, sticky="ew")
        bottom_frame.columnconfigure(0, weight=1)

        self.input_box = tk.Entry(
            bottom_frame,
            font=("Segoe UI", 12),
            bd=0,
            relief="flat",
            bg="#1f2937",
            fg="#f9fafb",
            insertbackground="#f9fafb",
        )
        self.input_box.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.input_box.bind("<Return>", self._send_message)

        send_button = tk.Button(
            bottom_frame,
            text="Send",
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6",
            fg="white",
            bd=0,
            padx=16,
            pady=8,
            activebackground="#2563eb",
            command=self._send_message,
        )
        send_button.grid(row=0, column=1)

        clear_button = tk.Button(
            bottom_frame,
            text="Clear Chat",
            font=("Segoe UI", 10),
            bg="#374151",
            fg="#f9fafb",
            bd=0,
            padx=12,
            pady=8,
            activebackground="#4b5563",
            command=self._clear_chat,
        )
        clear_button.grid(row=0, column=2, padx=(10, 0))

        self._append_message("assistant", "Hello! I am your AI FAQ assistant. Ask me a question and I will find the best answer from the knowledge base.")

    def _on_frame_configure(self, event) -> None:
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def _append_message(self, sender: str, message: str) -> None:
        # Render a chat bubble for either the user or the assistant.
        timestamp = datetime.now().strftime("%H:%M")
        bubble = tk.Frame(self.chat_window, bg="#111827", pady=6)
        bubble.pack(fill="x", padx=10, pady=4)

        if sender == "user":
            wrapper = tk.Frame(bubble, bg="#111827")
            wrapper.pack(anchor="e")
            content = tk.Label(
                wrapper,
                text=message,
                font=("Segoe UI", 11),
                fg="#f9fafb",
                bg="#2563eb",
                justify="left",
                wraplength=500,
                padx=12,
                pady=8,
            )
            content.pack()
            tk.Label(wrapper, text=timestamp, font=("Segoe UI", 8), fg="#94a3b8", bg="#111827").pack(anchor="e", pady=(2, 0))
        else:
            wrapper = tk.Frame(bubble, bg="#111827")
            wrapper.pack(anchor="w")
            content = tk.Label(
                wrapper,
                text=message,
                font=("Segoe UI", 11),
                fg="#f9fafb",
                bg="#1f2937",
                justify="left",
                wraplength=500,
                padx=12,
                pady=8,
            )
            content.pack()
            tk.Label(wrapper, text=timestamp, font=("Segoe UI", 8), fg="#94a3b8", bg="#111827").pack(anchor="w", pady=(2, 0))

        self.chat_window.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def _clear_chat(self) -> None:
        for widget in self.chat_window.winfo_children():
            widget.destroy()
        self._append_message("assistant", "Chat cleared. Ask me anything about the FAQ knowledge base.")

    def _send_message(self, event=None) -> None:
        # Capture the user's typed question and process it asynchronously.
        user_input = self.input_box.get().strip()
        if not user_input:
            return

        self.input_box.delete(0, tk.END)
        self._append_message("user", user_input)

        def response_task() -> None:
            try:
                response = self.engine.get_response(user_input)
            except Exception as exc:
                response = f"An unexpected error occurred: {exc}"
            self.root.after(0, lambda: self._append_message("assistant", response))

        threading.Thread(target=response_task, daemon=True).start()


def main() -> None:
    faq_path = str(Path(__file__).resolve().parent / "faq.json")
    root = tk.Tk()
    app = FAQChatbotGUI(root=root, faq_path=faq_path)
    root.mainloop()


if __name__ == "__main__":
    main()
