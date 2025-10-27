# main.py
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import (
    Color, RoundedRectangle, Ellipse, Line, PushMatrix, PopMatrix, Rotate, Rectangle
)
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.metrics import dp
from datetime import datetime
import math

class AnalogClock(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # refresh ~30 times per second for smooth second-hand movement
        Clock.schedule_interval(self.update_clock, 1.0 / 30.0)

    def draw_text(self, text, x, y, font_size):
        label = CoreLabel(text=str(text), font_size=font_size)
        label.refresh()
        texture = label.texture
        w, h = texture.size
        self.canvas.add(Rectangle(texture=texture, pos=(x - w / 2, y - h / 2), size=(w, h)))

    def on_size(self, *args):
        # redraw when the widget size changes
        self.update_clock(0)

    def update_clock(self, dt):
        self.canvas.clear()
        with self.canvas:
            # parameters
            w, h = self.width, self.height
            size = min(w, h)
            padding = dp(16)  # outer spacing
            corner_radius = size * 0.06
            face_size = size - 2 * padding
            center_x = self.x + w / 2
            center_y = self.y + h / 2
            face_left = center_x - face_size / 2
            face_bottom = center_y - face_size / 2

            # Colors
            white = (1, 1, 1)
            black = (0, 0, 0)
            gold = (0.86, 0.74, 0.28)  # a golden hue
            dark_gold = (0.65, 0.51, 0.12)

            # Outer golden rim (rounded square)
            Color(*dark_gold)
            RoundedRectangle(pos=(face_left - dp(8), face_bottom - dp(8)),
                             size=(face_size + dp(16), face_size + dp(16)),
                             radius=[corner_radius + dp(8)])

            # Outer border (thin dark rim)
            Color(*gold)
            RoundedRectangle(pos=(face_left - dp(6), face_bottom - dp(6)),
                             size=(face_size + dp(12), face_size + dp(12)),
                             radius=[corner_radius + dp(6)])

            # White clock face (rounded square)
            Color(*white)
            RoundedRectangle(pos=(face_left, face_bottom),
                             size=(face_size, face_size),
                             radius=[corner_radius])

            # Inner golden rim (thin)
            inset = dp(10)
            Color(*gold)
            RoundedRectangle(pos=(face_left + inset, face_bottom + inset),
                             size=(face_size - 2 * inset, face_size - 2 * inset),
                             radius=[corner_radius - dp(3)])
                             # Slight inner white disk to create an inner ring effect (so rim appears inside)
            inner_inset = dp(14)
            Color(*white)
            RoundedRectangle(pos=(face_left + inner_inset, face_bottom + inner_inset),
                             size=(face_size - 2 * inner_inset, face_size - 2 * inner_inset),
                             radius=[max(corner_radius - dp(7), 0)])

            # center and radius for hands (use circle inscribed in the square)
            radius = (face_size - 2 * inner_inset) / 2
            cx, cy = center_x, center_y

            # hour marks (numbers). place them in circle positions
            number_radius = radius * 0.82
            font_size = int(radius * 0.18)
            for hour in range(1, 13):
                angle_deg = 90 - (hour * 30)  # 12 at top (90 deg)
                rad = math.radians(angle_deg)
                nx = cx + number_radius * math.cos(rad)
                ny = cy + number_radius * math.sin(rad)
                Color(*black)
                self.draw_text(str(hour), nx, ny, font_size)

            # small minute ticks around edge
            tick_outer = radius + inner_inset * 0.4
            tick_inner_long = tick_outer - dp(14)  # for hour tick
            tick_inner_short = tick_outer - dp(8)
            for m in range(60):
                angle = math.radians(90 - m * 6)
                x1 = cx + tick_inner_short * math.cos(angle)
                y1 = cy + tick_inner_short * math.sin(angle)
                x2 = cx + tick_outer * math.cos(angle)
                y2 = cy + tick_outer * math.sin(angle)
                if m % 5 == 0:
                    x1 = cx + tick_inner_long * math.cos(angle)
                    y1 = cy + tick_inner_long * math.sin(angle)
                    Line(points=[x1, y1, x2, y2], width=dp(2))
                else:
                    Line(points=[x1, y1, x2, y2], width=dp(1))

            # time with fractions for smooth second hand
            now = datetime.now()
            sec = now.second + now.microsecond / 1_000_000.0
            minute = now.minute + sec / 60.0
            hour = (now.hour % 12) + minute / 60.0

            # angles in degrees (clockwise rotation from 12 o'clock)
            sec_angle_deg = 90 - sec * 6.0
            min_angle_deg = 90 - minute * 6.0
            hour_angle_deg = 90 - hour * 30.0

            # Draw hands using PushMatrix / Rotate for clean transforms
            # Second hand (thin, red)
            PushMatrix()
            rot = Rotate(angle=sec_angle_deg, origin=(cx, cy))
            Color(0.85, 0.1, 0.15)  # reddish
            Line(points=[cx, cy, cx + radius * 0.9 * math.cos(math.radians(sec_angle_deg)),
                         cy + radius * 0.9 * math.sin(math.radians(sec_angle_deg))],
                 width=dp(1.6), cap='round')
            PopMatrix()

            # Minute hand (black slender)
            PushMatrix()
            rotn = Rotate(angle=min_angle_deg, origin=(cx, cy))
            Color(*black)
            Line(points=[cx, cy, cx + radius * 0.75 * math.cos(math.radians(min_angle_deg)),
                         cy + radius * 0.75 * math.sin(math.radians(min_angle_deg))],
                 width=dp(3), cap='round')
            PopMatrix()

            # Hour hand (black thicker)
            PushMatrix()
            roth = Rotate(angle=hour_angle_deg, origin=(cx, cy))
            Color(*black)
            Line(points=[cx, cy, cx + radius * 0.48 * math.cos(math.radians(hour_angle_deg)),
                         cy + radius * 0.48 * math.sin(math.radians(hour_angle_deg))],
                 width=dp(5), cap='round')
            PopMatrix()

            # center pin (small golden disc with darker border)
            Color(*gold)
            Ellipse(pos=(cx - dp(8), cy - dp(8)), size=(dp(16), dp(16)))
            Color(*dark_gold)
            Ellipse(pos=(cx - dp(4), cy - dp(4)), size=(dp(8), dp(8)))

            # optional digital time at bottom (small)
            Color(0, 0, 0)
            time_text = now.strftime("%I:%M:%S %p")
            self.draw_text(time_text, cx, cy - radius * 0.65, int(radius * 0.12))

class ClockApp(App):
    def build(self):
        root = AnalogClock()
        # keep a square aspect ratio by binding to window size
        root.size_hint = (None, None)
        from kivy.core.window import Window
        # set nice initial window
        target = min(Window.width, Window.height) * 0.9
        root.size = (target, target)
        root.pos = ((Window.width - root.width) / 2.0, (Window.height - root.height) / 2.0)

        # respond to window resize to keep the clock centered
        def on_win_resize(win, w, h):
            s = min(w, h) * 0.9
            root.size = (s, s)
            root.pos = ((w - s) / 2.0, (h - s) / 2.0)
        Window.bind(on_resize=on_win_resize)
        return root

if __name__ == "__main__":
    ClockApp().run()
