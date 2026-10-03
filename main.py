import time
import threading
import tkinter as tk
from tkinter import messagebox
from amp import Bot


class HostBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FIRE R PUBLICATIONS • HOST BOT 1.0")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b0f14")

        self.bot = None
        self.running = False

        # =========================
        # COLORS
        # =========================
        BG = "#0b0f14"
        CARD = "#121820"
        ENTRY = "#1a232e"
        TEXT = "#ffffff"
        MUTED = "#8994a3"
        ACCENT = "#00d9ff"
        GREEN = "#20e070"
        RED = "#ff4d5d"

        # =========================
        # HEADER
        # =========================
        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=(25, 5))

        tk.Label(
            header,
            text="FIRE R",
            font=("Segoe UI", 25, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack()

        tk.Label(
            header,
            text="PUBLICATIONS",
            font=("Segoe UI", 11, "bold"),
            fg=MUTED,
            bg=BG
        ).pack()

        tk.Label(
            header,
            text="HOST BOT 1.0",
            font=("Segoe UI", 14, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(pady=(8, 0))

        # =========================
        # SETTINGS CARD
        # =========================
        settings = tk.Frame(
            root,
            bg=CARD,
            highlightthickness=1,
            highlightbackground="#26313d"
        )
        settings.pack(fill="x", padx=35, pady=20)

        tk.Label(
            settings,
            text="SERVER CONFIGURATION",
            font=("Segoe UI", 11, "bold"),
            fg=ACCENT,
            bg=CARD
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(18, 15)
        )

        # Function for creating fields
        def create_field(row, label, value):
            tk.Label(
                settings,
                text=label,
                font=("Segoe UI", 10, "bold"),
                fg=MUTED,
                bg=CARD
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=20,
                pady=8
            )

            entry = tk.Entry(
                settings,
                width=38,
                font=("Segoe UI", 10),
                bg=ENTRY,
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )
            entry.grid(
                row=row,
                column=1,
                padx=(10, 20),
                pady=8,
                ipady=7
            )
            entry.insert(0, value)

            return entry

        self.host_entry = create_field(
            1,
            "Server Address",
            "CrashedSMP.aternos.me"
        )

        self.port_entry = create_field(
            2,
            "Port",
            "13928"
        )

        self.username_entry = create_field(
            3,
            "Bot Name",
            "HOST"
        )

        self.version_entry = create_field(
            4,
            "Server Version",
            "26.2"
        )

        tk.Frame(
            settings,
            height=10,
            bg=CARD
        ).grid(row=5, column=0, columnspan=2)

        # =========================
        # STATUS
        # =========================
        status_card = tk.Frame(
            root,
            bg=CARD,
            highlightthickness=1,
            highlightbackground="#26313d"
        )
        status_card.pack(fill="x", padx=35, pady=(0, 15))

        tk.Label(
            status_card,
            text="BOT STATUS",
            font=("Segoe UI", 10, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(pady=(12, 2))

        self.status_label = tk.Label(
            status_card,
            text="● OFFLINE",
            font=("Segoe UI", 14, "bold"),
            fg=RED,
            bg=CARD
        )
        self.status_label.pack(pady=(0, 12))

        # =========================
        # BUTTONS
        # =========================
        buttons = tk.Frame(root, bg=BG)
        buttons.pack(pady=5)

        self.start_button = tk.Button(
            buttons,
            text="▶  START BOT",
            command=self.start_bot,
            font=("Segoe UI", 10, "bold"),
            bg=GREEN,
            fg="#06100a",
            activebackground=GREEN,
            activeforeground="#06100a",
            relief="flat",
            bd=0,
            width=18,
            height=2,
            cursor="hand2"
        )
        self.start_button.grid(row=0, column=0, padx=8)

        self.stop_button = tk.Button(
            buttons,
            text="■  STOP BOT",
            command=self.stop_bot,
            font=("Segoe UI", 10, "bold"),
            bg=RED,
            fg="white",
            activebackground=RED,
            activeforeground="white",
            relief="flat",
            bd=0,
            width=18,
            height=2,
            cursor="hand2",
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=8)

        # =========================
        # LOG
        # =========================
        log_card = tk.Frame(
            root,
            bg=CARD,
            highlightthickness=1,
            highlightbackground="#26313d"
        )
        log_card.pack(fill="both", expand=True, padx=35, pady=15)

        tk.Label(
            log_card,
            text="LIVE BOT CONSOLE",
            font=("Segoe UI", 10, "bold"),
            fg=ACCENT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.log_box = tk.Text(
            log_card,
            height=7,
            font=("Consolas", 9),
            bg="#080c11",
            fg="#b9c5d3",
            insertbackground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=8,
            state="disabled"
        )
        self.log_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # =========================
        # FOOTER
        # =========================
        tk.Label(
            root,
            text="FIRE R PUBLICATIONS  •  Minecraft HOST Bot",
            font=("Segoe UI", 8),
            fg="#566170",
            bg=BG
        ).pack(pady=(0, 12))

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # =========================
    # LOG
    # =========================
    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    # =========================
    # START BOT
    # =========================
    def start_bot(self):

        if self.running:
            return

        host = self.host_entry.get().strip()
        port_text = self.port_entry.get().strip()
        username = self.username_entry.get().strip()
        version = self.version_entry.get().strip()

        if not host or not port_text or not username or not version:
            messagebox.showerror(
                "Missing Information",
                "Please fill all server settings."
            )
            return

        try:
            port = int(port_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Port",
                "Port must be a number."
            )
            return

        self.running = True

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.status_label.config(
            text="● CONNECTING...",
            fg="#ffd166"
        )

        self.log("----------------------------------------")
        self.log("Starting HOST Bot...")
        self.log(f"Server: {host}:{port}")
        self.log(f"Bot Name: {username}")
        self.log(f"Version: {version}")

        thread = threading.Thread(
            target=self.run_bot,
            args=(host, port, username, version),
            daemon=True
        )

        thread.start()

    # =========================
    # BOT
    # =========================
    def run_bot(self, host, port, username, version):

        CONFIG = {
            "host": host,
            "port": port,
            "version": version,
            "username": username,
            "game_mode": "creative",
            "auth_session": None,
            "session_joiner": None,
            "model_optional": True,
        }

        try:

            self.bot = Bot(CONFIG)

            self.bot.start()

            self.log(f"{username} joined the server!")

            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="● ONLINE",
                    fg="#20e070"
                )
            )

            self.bot._executor.enque_command({
                "action": "chat",
                "message": "WELCOME TO CRASHED SMP"
            })

            self.log("Welcome message sent!")
            self.log(f"{username} is running.")

            while self.running:
                time.sleep(1)

        except Exception as e:

            self.log(f"ERROR: {e}")

            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="● ERROR",
                    fg="#ff4d5d"
                )
            )

            self.running = False

        finally:

            self.root.after(
                0,
                lambda: self.start_button.config(state="normal")
            )

            self.root.after(
                0,
                lambda: self.stop_button.config(state="disabled")
            )

    # =========================
    # STOP
    # =========================
    def stop_bot(self):

        if not self.running:
            return

        self.running = False

        self.log("Stopping HOST...")

        try:
            if self.bot:
                self.bot.disconnect()
        except Exception as e:
            self.log(f"Disconnect error: {e}")

        self.bot = None

        self.status_label.config(
            text="● OFFLINE",
            fg="#ff4d5d"
        )

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

        self.log("HOST stopped.")
        self.log("----------------------------------------")

    # =========================
    # CLOSE
    # =========================
    def close_app(self):

        if self.running:
            self.stop_bot()

        self.root.destroy()


# =========================
# MAIN
# =========================
def main():

    root = tk.Tk()

    HostBotApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()