import time
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from kivy.graphics import Color, RoundedRectangle, Line

from amp import Bot


# =========================================================
# COLORS
# =========================================================

BG = (0.055, 0.065, 0.09, 1)
CARD = (0.09, 0.105, 0.14, 1)
CARD_2 = (0.12, 0.135, 0.18, 1)
TEXT = (0.94, 0.96, 1, 1)
SUBTEXT = (0.60, 0.65, 0.73, 1)
GREEN = (0.20, 0.85, 0.45, 1)
RED = (0.95, 0.28, 0.30, 1)
BLUE = (0.25, 0.55, 1, 1)


# =========================================================
# ROUNDED BACKGROUND
# =========================================================

class RoundedBox(BoxLayout):

    def __init__(self, bg_color=CARD, radius=15, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = bg_color
        self.radius = radius

        with self.canvas.before:
            Color(*self.bg_color)

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(self.radius)]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# =========================================================
# MAIN APP
# =========================================================

class HostBotApp(App):

    def build(self):

        Window.clearcolor = BG

        self.bot = None
        self.running = False

        self.x = 0
        self.y = 0
        self.z = 0

        # -------------------------------------------------
        # ROOT
        # -------------------------------------------------

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=[dp(15), dp(10)],
            spacing=dp(2),
            size_hint_y=None,
            height=dp(82)
        )

        title = Label(
            text="HOST BOT",
            color=TEXT,
            font_size="25sp",
            bold=True,
            size_hint_y=None,
            height=dp(36)
        )

        subtitle = Label(
            text="ANDROID VERSION 1.0",
            color=BLUE,
            font_size="12sp",
            bold=True,
            size_hint_y=None,
            height=dp(22)
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        root.add_widget(header)

        # -------------------------------------------------
        # SCROLL AREA
        # -------------------------------------------------

        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(4)
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            padding=[0, dp(2)]
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # -------------------------------------------------
        # SERVER SETTINGS CARD
        # -------------------------------------------------

        settings_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(280)
        )

        settings_title = Label(
            text="SERVER SETTINGS",
            color=TEXT,
            font_size="15sp",
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(28)
        )

        settings_card.add_widget(settings_title)

        self.host_input = self.make_input(
            "Server Address",
            "CrashedSMP.aternos.me"
        )
        settings_card.add_widget(self.host_input)

        self.port_input = self.make_input(
            "Port",
            "13928",
            numeric=True
        )
        settings_card.add_widget(self.port_input)

        self.name_input = self.make_input(
            "Bot Name",
            "HOST"
        )
        settings_card.add_widget(self.name_input)

        self.version_input = self.make_input(
            "Minecraft Version",
            "26.2"
        )
        settings_card.add_widget(self.version_input)

        content.add_widget(settings_card)

        # -------------------------------------------------
        # STATUS CARD
        # -------------------------------------------------

        status_card = RoundedBox(
            bg_color=CARD,
            orientation="horizontal",
            padding=[dp(12), dp(8)],
            size_hint_y=None,
            height=dp(65)
        )

        status_text_box = BoxLayout(
            orientation="vertical"
        )

        status_label = Label(
            text="BOT STATUS",
            color=SUBTEXT,
            font_size="11sp",
            halign="left"
        )

        self.status = Label(
            text="● OFFLINE",
            color=RED,
            font_size="18sp",
            bold=True,
            halign="left"
        )

        status_text_box.add_widget(status_label)
        status_text_box.add_widget(self.status)

        status_card.add_widget(status_text_box)

        content.add_widget(status_card)

        # -------------------------------------------------
        # START / STOP
        # -------------------------------------------------

        buttons = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(55)
        )

        start_button = Button(
            text="▶  START BOT",
            font_size="14sp",
            bold=True,
            background_normal="",
            background_color=GREEN,
            color=(0.02, 0.04, 0.03, 1)
        )

        start_button.bind(
            on_press=self.start_bot
        )

        stop_button = Button(
            text="■  STOP BOT",
            font_size="14sp",
            bold=True,
            background_normal="",
            background_color=RED,
            color=TEXT
        )

        stop_button.bind(
            on_press=self.stop_bot
        )

        buttons.add_widget(start_button)
        buttons.add_widget(stop_button)

        content.add_widget(buttons)

        # -------------------------------------------------
        # CUSTOM CHAT CARD
        # -------------------------------------------------

        chat_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(155)
        )

        chat_title = Label(
            text="CUSTOM CHAT",
            color=TEXT,
            font_size="15sp",
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(28)
        )

        chat_card.add_widget(chat_title)

        self.chat_input = TextInput(
            hint_text="Write a message...",
            multiline=False,
            font_size="14sp",
            padding=[dp(12), dp(12)],
            background_normal="",
            background_color=CARD_2,
            foreground_color=TEXT,
            hint_text_color=SUBTEXT,
            cursor_color=BLUE,
            size_hint_y=None,
            height=dp(48)
        )

        chat_card.add_widget(self.chat_input)

        send_button = Button(
            text="SEND CHAT",
            font_size="14sp",
            bold=True,
            background_normal="",
            background_color=BLUE,
            color=TEXT,
            size_hint_y=None,
            height=dp(45)
        )

        send_button.bind(
            on_press=self.send_custom_chat
        )

        chat_card.add_widget(send_button)

        content.add_widget(chat_card)

        # -------------------------------------------------
        # AUTOMATIC FEATURES
        # -------------------------------------------------

        auto_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=dp(12),
            spacing=dp(5),
            size_hint_y=None,
            height=dp(115)
        )

        auto_title = Label(
            text="AUTOMATIC FEATURES",
            color=TEXT,
            font_size="15sp",
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(28)
        )

        auto_card.add_widget(auto_title)

        auto_chat = Label(
            text="💬  Welcome Chat     →     Every 60 seconds",
            color=SUBTEXT,
            font_size="13sp",
            halign="left"
        )

        auto_move = Label(
            text="🚶  Movement + Jump  →     Every 10 seconds",
            color=SUBTEXT,
            font_size="13sp",
            halign="left"
        )

        auto_card.add_widget(auto_chat)
        auto_card.add_widget(auto_move)

        content.add_widget(auto_card)

        # -------------------------------------------------
        # CONSOLE CARD
        # -------------------------------------------------

        console_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=dp(12),
            spacing=dp(7),
            size_hint_y=None,
            height=dp(300)
        )

        console_title = Label(
            text="LIVE CONSOLE",
            color=TEXT,
            font_size="15sp",
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(28)
        )

        console_card.add_widget(console_title)

        console_scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(3)
        )

        self.console = Label(
            text="HOST Bot ready...\n",
            color=SUBTEXT,
            font_size="12sp",
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.console.bind(
            texture_size=self.update_console_height
        )

        console_scroll.add_widget(self.console)
        console_card.add_widget(console_scroll)

        content.add_widget(console_card)

        # -------------------------------------------------
        # FOOTER
        # -------------------------------------------------

        footer = Label(
            text="FIRE R PUBLICATIONS  •  HOST BOT 1.0",
            color=SUBTEXT,
            font_size="10sp",
            size_hint_y=None,
            height=dp(30)
        )

        content.add_widget(footer)

        scroll.add_widget(content)

        root.add_widget(scroll)

        return root

    # =====================================================
    # INPUT CREATOR
    # =====================================================

    def make_input(self, hint, default="", numeric=False):

        box = TextInput(
            text=default,
            hint_text=hint,
            multiline=False,
            font_size="14sp",
            padding=[dp(12), dp(12)],
            background_normal="",
            background_color=CARD_2,
            foreground_color=TEXT,
            hint_text_color=SUBTEXT,
            cursor_color=BLUE,
            size_hint_y=None,
            height=dp(45)
        )

        if numeric:
            box.input_filter = "int"

        return box

    # =====================================================
    # CONSOLE
    # =====================================================

    def update_console_height(self, instance, value):

        instance.height = value[1]

    def log(self, message):

        def update(_dt):

            self.console.text += str(message) + "\n"

        Clock.schedule_once(update)

    # =====================================================
    # START BOT
    # =====================================================

    def start_bot(self, instance):

        if self.running:

            self.log("HOST is already running.")
            return

        host = self.host_input.text.strip()
        port_text = self.port_input.text.strip()
        username = self.name_input.text.strip()
        version = self.version_input.text.strip()

        if not host:
            self.log("Server address is empty.")
            return

        if not username:
            self.log("Bot name is empty.")
            return

        try:

            port = int(port_text)

        except ValueError:

            self.log("Invalid port.")
            return

        self.running = True

        self.status.text = "● CONNECTING..."
        self.status.color = BLUE

        thread = threading.Thread(
            target=self.run_bot,
            args=(host, port, username, version),
            daemon=True
        )

        thread.start()

    # =====================================================
    # RUN BOT
    # =====================================================

    def run_bot(
        self,
        host,
        port,
        username,
        version
    ):

        try:

            config = {
                "host": host,
                "port": port,
                "version": version,
                "username": username,

                "game_mode": "creative",

                "auth_session": None,
                "session_joiner": None,

                "model_optional": True,
            }

            self.log("================================")
            self.log("HOST BOT 1.0")
            self.log("Connecting...")
            self.log(f"Server: {host}:{port}")
            self.log(f"Bot Name: {username}")
            self.log(f"Version: {version}")
            self.log("================================")

            self.bot = Bot(config)

            self.bot.start()

            self.log(
                f"{username} joined the server!"
            )

            Clock.schedule_once(
                lambda dt: self.set_online()
            )

            # Initial welcome
            time.sleep(2)

            self.send_welcome()

            # Start automatic tasks
            self.background_tasks()

        except Exception as e:

            self.log(
                f"BOT ERROR: {e}"
            )

            self.running = False
            self.bot = None

            Clock.schedule_once(
                lambda dt: self.set_offline()
            )

    # =====================================================
    # ONLINE
    # =====================================================

    def set_online(self):

        self.status.text = "● ONLINE"
        self.status.color = GREEN

    # =====================================================
    # OFFLINE
    # =====================================================

    def set_offline(self):

        self.status.text = "● OFFLINE"
        self.status.color = RED

    # =====================================================
    # WELCOME CHAT
    # =====================================================

    def send_welcome(self):

        if not self.bot:
            return

        try:

            self.bot._executor.enque_command({
                "action": "chat",
                "message": "WELCOME TO CRASHED SMP"
            })

            self.log(
                "Welcome message sent!"
            )

        except Exception as e:

            self.log(
                f"Welcome chat error: {e}"
            )

    # =====================================================
    # CUSTOM CHAT
    # =====================================================

    def send_custom_chat(self, instance):

        message = self.chat_input.text.strip()

        if not message:

            self.log(
                "Write a message first."
            )

            return

        if not self.bot or not self.running:

            self.log(
                "HOST is not online."
            )

            return

        try:

            self.bot._executor.enque_command({
                "action": "chat",
                "message": message
            })

            self.log(
                f"CHAT → {message}"
            )

            self.chat_input.text = ""

        except Exception as e:

            self.log(
                f"Chat error: {e}"
            )

    # =====================================================
    # BACKGROUND TASKS
    # =====================================================

    def background_tasks(self):

        last_welcome = time.time()
        last_action = time.time()

        while self.running:

            try:

                now = time.time()

                # -----------------------------------------
                # REPEAT CHAT EVERY 60 SECONDS
                # -----------------------------------------

                if now - last_welcome >= 60:

                    self.send_welcome()

                    last_welcome = now

                # -----------------------------------------
                # MOVEMENT + JUMP EVERY 10 SECONDS
                # -----------------------------------------

                if now - last_action >= 10:

                    self.simple_move()

                    time.sleep(0.5)

                    self.simple_jump()

                    last_action = now

                time.sleep(1)

            except Exception as e:

                self.log(
                    f"Background error: {e}"
                )

                time.sleep(2)

    # =====================================================
    # SIMPLE MOVEMENT
    # =====================================================

    def simple_move(self):

        if not self.bot:
            return

        try:

            self.x += 1

            self.bot._executor.enque_command({
                "action": "move",
                "x": self.x,
                "y": self.y,
                "z": self.z,
                "on_ground": True,
                "delay": 0.2
            })

            self.log(
                "HOST moved forward."
            )

        except Exception as e:

            self.log(
                f"Movement error: {e}"
            )

    # =====================================================
    # JUMP
    # =====================================================

    def simple_jump(self):

        if not self.bot:
            return

        try:

            self.bot._executor.enque_command({
                "action": "jump",
                "delay": 0.2
            })

            self.log(
                "HOST jumped."
            )

        except Exception as e:

            self.log(
                f"Jump error: {e}"
            )

    # =====================================================
    # STOP BOT
    # =====================================================

    def stop_bot(self, instance):

        if not self.running:

            self.log(
                "HOST is already stopped."
            )

            return

        self.running = False

        self.log(
            "Stopping HOST..."
        )

        try:

            if self.bot:

                if hasattr(self.bot, "stop"):

                    self.bot.stop()

                elif hasattr(self.bot, "disconnect"):

                    self.bot.disconnect()

        except Exception as e:

            self.log(
                f"Stop error: {e}"
            )

        self.bot = None

        self.set_offline()

        self.log(
            "HOST stopped."
        )


# =========================================================
# START APP
# =========================================================

if __name__ == "__main__":
    HostBotApp().run()