import os
from kivy.config import Config

Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'maxfps', '30')

import datetime as dt
import time
import numpy as np
import os
from kivy.utils import platform

if platform == "android":
    BASE = os.path.dirname(__file__)
else:
    BASE = "."

path = os.path.join(BASE, "ride_policy.npz")
data = np.load(path, allow_pickle=True)

w0 = data["0.0.weight"]
b0 = data["0.0.bias"]

w2 = data["0.2.weight"]
b2 = data["0.2.bias"]

w4 = data["1.weight"]
b4 = data["1.bias"]

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, RoundedRectangle
Window.clearcolor = (1, 1, 1, 1)  # White background

from queue_api import fetch_live_data, get_ride_info
from rides_config import rides, ride_time, walk_time

PARK_OPEN = 10 * 60
PARK_CLOSE = 18 * 60

ride_to_index = {r: i for i, r in enumerate(rides)}

def predict(obs):
    x = np.asarray(obs, dtype=np.float32)

    # Layer 1
    x = np.tanh(x @ w0.T + b0)

    # Layer 2
    x = np.tanh(x @ w2.T + b2)

    # Output layer (37 actions)
    logits = x @ w4.T + b4

    return logits

class DarkCheckBox(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.checked = False
        self.text = ""

        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))

        self.font_size = dp(24)
        self.bold = True

        self.halign = "center"
        self.valign = "middle"

        self.bind(on_press=self.toggle)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[6]
            )

        with self.canvas.after:
            Color(0, 0, 0, 1)
            self.border_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, 6),
                width=2
            )

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        self.border_line.rounded_rectangle = (
            self.x, self.y,
            self.width, self.height,
            6
        )

        # 🔥 THIS IS THE KEY FIX
        self.text_size = self.size
        self.font_size = self.height * 0.6

    def toggle(self, *args):
        self.checked = not self.checked
        self.text = "X" if self.checked else ""

class RideRow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            # White fill
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20]
            )

        with self.canvas.after:
            # Black border
            Color(0, 0, 0, 1)
            self.border_line = Line(
                rounded_rectangle=(
                    self.x, self.y,
                    self.width, self.height,
                    10
                ),
                width=1.2
            )

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        self.font_size = self.height * 0.6
        self.text_size = self.size

        self.border_line.rounded_rectangle = (
            self.x, self.y,
            self.width, self.height,
            4
        )
# ---------------- MODEL SCREEN MANAGER ----------------
class MainSM(ScreenManager):
    pass


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(10),
            size_hint_y=None
        )

        content.bind(minimum_height=content.setter("height"))

        # --- BANNER (mobile safe) ---
        banner = Image(
            source=os.path.join(BASE, "TheSmiler.webp"),
            size_hint=(1, None),
            height=dp(220),
            allow_stretch=True,
            keep_ratio=False
        )

        title = Label(
            text="Ride Planner",
            font_size="24sp",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(60)
        )

        parkname = Label(
            text="Select your theme park",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(44)
        )

        start_btn = Button(
            text="Alton Towers",
            size_hint=(1, None),
            height=dp(60)
        )
        start_btn.bind(on_press=self.open_setup)

        content.add_widget(banner)
        content.add_widget(title)
        content.add_widget(parkname)
        content.add_widget(start_btn)

        scroll.add_widget(content)
        self.add_widget(scroll)
    
    def open_setup(self, *_):
        App.get_running_app().sm.current = "setup"

# ---------------- SCREEN 1 (SETUP) ----------------
class SetupScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_size = "24sp"
        self.bold = True
        self.halign = "center"
        self.valign = "middle"
        self.text_size = self.size

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        scroll = ScrollView(bar_width=dp(6))

        layout.add_widget(Label(
            text="Select rides you want to do:",
            size_hint_y=None,
            height=40,
            color=(0, 0, 0, 1)
        ))

        self.ride_checks = {}

        scroll = ScrollView(size_hint=(1, 1))

        ride_grid = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        ride_grid.bind(minimum_height=ride_grid.setter("height"))

        for ride in rides:
            row = RideRow(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(60),
                padding=5
            )
            cb = DarkCheckBox()
            cb.size = (dp(44), dp(44))

            lbl = Label(
                text=ride,
                halign="left",
                color=(0, 0, 0, 1)
            )
            self.ride_checks[ride] = cb
            row.add_widget(cb)
            row.add_widget(lbl)

            ride_grid.add_widget(row)

        scroll.add_widget(ride_grid)
        layout.add_widget(scroll)

        self.completed_spinner = Spinner(
            text="Current ride location (optional)",
            values=rides,
            size_hint=(1, None),
            height=dp(50)
        )

        layout.add_widget(self.completed_spinner)

        start_btn = Button(
            text="Start Planner",
            size_hint_y=None,
            height=50
        )
        start_btn.bind(on_press=self.start)

        layout.add_widget(start_btn)

        self.add_widget(layout)

    def start(self, _):
        app = App.get_running_app()

        app.required_rides = [
            ride
            for ride, cb in self.ride_checks.items()
            if cb.checked
        ]

        if not app.required_rides:
            print("Select at least one ride")
            return

        app.done_required = set()

        if self.completed_spinner.text in rides:
            app.done_required.add(self.completed_spinner.text)
            if self.completed_spinner.text in app.required_rides:
                app.required_rides.remove(self.completed_spinner.text)            
            app.current = rides.index(self.completed_spinner.text)
        else:
            app.current = 0

        now = dt.datetime.now()
        app.time_min = max(PARK_OPEN, now.hour * 60 + now.minute)

        app.last_obs = None
        app.sm.current = "planner"

# ---------------- SCREEN 2 (PLANNER) ----------------
class PlannerScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical")

        self.log = TextInput(
            readonly=True,
            font_size="14sp"
        )

        back_btn = Button(
            text="Back",
            size_hint_y=None,
            height=dp(60)
        )
        back_btn.bind(on_press=self.go_back)

        root.add_widget(self.log)
        root.add_widget(back_btn)

        self.add_widget(root)

    def on_enter(self):
        self.log.text = "=== LIVE ITINERARY ===\n"
        self.event = Clock.schedule_interval(self.step, 2)
        def on_leave(self):
            if hasattr(self, "event"):
                self.event.cancel()

    def on_leave(self):
        Clock.unschedule(self.step)

    def write(self, text):
        self.log.text += text + "\n"

    def go_back(self, _):
        App.get_running_app().sm.current = "home"

    def step(self, dt):

        app = App.get_running_app()

        # ---------------- TIME CHECK ----------------
        if app.time_min >= PARK_CLOSE:
            self.write("Park closed")
            return False

        # ---------------- GET LIVE DATA ----------------
        try:
            data = fetch_live_data()
        except:
            self.write("API error")
            return True
        if data is None:
            self.write("API unavailable")
            return False

        # ---------------- OPEN RIDES ----------------
        open_rides = [
            r for r in rides
            if get_ride_info(data, r)[0]
        ]

        if not open_rides:
            self.write("No rides open")
            return False

        # ---------------- OBS + MODEL ----------------
        obs = self.build_obs(app, open_rides)
        logits = predict(obs)

        # ---------------- CANDIDATES ----------------
        candidates = [r for r in open_rides if r in app.required_rides]
        if not candidates:
            candidates = open_rides

        # ---------------- PICK RIDE ----------------
        ride = max(
            candidates,
            key=lambda r: logits[ride_to_index[r]]
        )

        # ---------------- QUEUE + TIME ----------------
        _, queue = get_ride_info(data, ride)
        queue = max(queue or 5, 5)

        current = rides[app.current]

        walk = walk_time.get(current, {}).get(ride, 5)
        duration = ride_time.get(ride, 3)

        app.time_min += queue + walk + duration
        app.current = ride_to_index[ride]

        # ---------------- UPDATE STATE ----------------
        app.done_required.add(ride)
        if ride in app.required_rides:
            app.required_rides.remove(ride)

        # ---------------- LOG ----------------
        h = int(app.time_min // 60)
        m = int(app.time_min % 60)

        self.write(f"{h:02d}:{m:02d} → {ride} | Q:{queue} W:{walk}")

        if not app.required_rides:
            self.write("All required rides completed!")
            return False

        return True

    def build_obs(self, app, open_rides):
        obs = np.zeros(4 + len(rides), dtype=np.float32)

        # ---------------- GLOBAL STATE ----------------
        obs[0] = app.time_min / 600.0              # time normalised (rough)
        obs[1] = len(open_rides) / len(rides)                       # crowd placeholder (you don’t have live model yet)
        obs[2] = app.current / len(rides)          # current ride index

        total_required = max(1, len(app.required_rides))
        done = len(app.done_required)
        obs[3] = done / total_required             # progress

        # ---------------- RIDE MASK ----------------
        for i, r in enumerate(rides):
            if r in app.required_rides and r not in app.done_required:
                obs[4 + i] = 1.0
            else:
                obs[4 + i] = 0.0

        return obs


# ---------------- APP ----------------
class RidePlannerApp(App):

    def build(self):
        self.sm = MainSM()

        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SetupScreen(name="setup"))
        self.sm.add_widget(PlannerScreen(name="planner"))

        self.sm.current = "home"

        return self.sm


if __name__ == "__main__":
    RidePlannerApp().run()