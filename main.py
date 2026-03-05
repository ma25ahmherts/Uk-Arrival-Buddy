from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
import database

# Window Configuration
Window.size = (400, 700)

# Database Connection
database.connect()

# ---------- Styled Input Component ----------
class StyledInput(BoxLayout):
    def __init__(self, label_text, hint, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.size_hint_y = None
        self.height = 90  # Total height for label + input box

        # Field Label
        lbl = Label(
            text=label_text, 
            font_size=14, 
            color=(0.1, 0.1, 0.1, 1), 
            halign='left', 
            text_size=(320, None), 
            bold=True
        )
        
        # Input Field Style (Fixed padding and height for visibility)
        self.ti = TextInput(
            hint_text=hint, 
            multiline=False, 
            padding=[15, 12, 15, 12],  # Adjusted padding to center text vertically
            background_normal="",
            background_active="",
            background_color=(0.96, 0.96, 0.98, 1), 
            font_size=16,             
            foreground_color=(0, 0, 0, 1), 
            hint_text_color=(0.6, 0.6, 0.6, 1), 
            cursor_color=(0.1, 0.4, 1, 1),
            size_hint_y=None,
            height=50  # Fixed height for the input box area
        )
        
        self.add_widget(lbl)
        self.add_widget(self.ti)

# ---------------- Welcome Screen ----------------
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.4, 0.1, 0.9, 1) 
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        root = AnchorLayout(anchor_x='center', anchor_y='center')
        
        card = BoxLayout(orientation='vertical', padding=[30, 40], spacing=20, size_hint=(0.88, 0.7))
        with card.canvas.before:
            Color(1, 1, 1, 1)
            self.card_bg = RoundedRectangle(radius=[25])
        card.bind(pos=self.update_card, size=self.update_card)

        title = Label(text="Soul Speak", font_size=38, bold=True, color=(0.1, 0.1, 0.2, 1))
        sub_title = Label(text="Supporting International Students in the UK", font_size=14, color=(0.4, 0.4, 0.4, 1), halign="center")
        
        desc = Label(
            text="A smart digital assistant designed to guide new students\nthrough UK arrival, compliance, and essential setup steps.",
            font_size=13, halign="center", color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=100
        )

        btn = Button(
            text="Get Started", size_hint=(1, None), height=60,
            background_normal="", background_color=(0.1, 0.4, 1, 1), font_size=18, bold=True
        )
        with btn.canvas.before:
            Color(0.1, 0.4, 1, 1)
            self.btn_bg = RoundedRectangle(radius=[15])
        btn.bind(pos=self.update_btn, size=self.update_btn)
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'visa'))

        version = Label(text="Version: SRALM1", font_size=11, color=(0.7, 0.7, 0.7, 1))

        card.add_widget(title)
        card.add_widget(sub_title)
        card.add_widget(desc)
        card.add_widget(btn)
        card.add_widget(version)

        root.add_widget(card)
        self.add_widget(root)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def update_card(self, instance, value):
        self.card_bg.pos = instance.pos
        self.card_bg.size = instance.size

    def update_btn(self, instance, value):
        self.btn_bg.pos = instance.pos
        self.btn_bg.size = instance.size

# ---------------- Visa Screen ----------------
class VisaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.94, 0.96, 1, 1) 
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        root = AnchorLayout(anchor_x='center', anchor_y='center')
        
        card = BoxLayout(orientation='vertical', padding=[25, 25], spacing=15, size_hint=(0.92, 0.92))
        with card.canvas.before:
            Color(1, 1, 1, 1)
            self.card_bg = RoundedRectangle(radius=[20])
        card.bind(pos=self.update_card, size=self.update_card)

        icon = Label(text="🛡️", font_size=55, size_hint_y=None, height=70)
        header = Label(text="Verify Student Visa Status", font_size=22, bold=True, color=(0,0,0,1), size_hint_y=None, height=40)
        sub_header = Label(text="Secure UKVI verification for international students", font_size=12, color=(0.5,0.5,0.5,1), size_hint_y=None, height=30)

        card.add_widget(icon)
        card.add_widget(header)
        card.add_widget(sub_header)
        
        # Input Fields
        self.email_field = StyledInput("Email Address", "Enter email address")
        self.dob_field = StyledInput("Date of Birth", "DD / MM / YYYY")
        self.passport_field = StyledInput("Passport Number", "Enter passport number")

        card.add_widget(self.email_field)
        card.add_widget(self.dob_field)
        card.add_widget(self.passport_field)

        btn = Button(text="Verify Visa Status", size_hint_y=None, height=55, background_normal="", background_color=(0.1, 0.4, 1, 1), bold=True)
        with btn.canvas.before:
            Color(0.1, 0.4, 1, 1)
            self.btn_bg_v = RoundedRectangle(radius=[15])
        btn.bind(pos=self.update_btn_v, size=self.update_btn_v)
        btn.bind(on_press=self.save_data)
        
        footer = Label(text="Your information is secure and encrypted.", font_size=11, color=(0.6, 0.6, 0.6, 1))

        card.add_widget(Widget(size_hint_y=None, height=5))
        card.add_widget(btn)
        card.add_widget(footer)

        root.add_widget(card)
        self.add_widget(root)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def update_card(self, instance, value):
        self.card_bg.pos = instance.pos
        self.card_bg.size = instance.size

    def update_btn_v(self, instance, value):
        self.btn_bg_v.pos = instance.pos
        self.btn_bg_v.size = instance.size

    def save_data(self, instance):
        email = self.email_field.ti.text
        dob = self.dob_field.ti.text
        passport = self.passport_field.ti.text
        if email and dob and passport:
            database.save_verification(email, dob, passport)
            self.manager.current = "main"

# ---------------- Main Screen ----------------
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(size=Window.size, pos=self.pos)
        self.add_widget(Label(text="Dashboard Ready", color=(0,0,0,1)))

# ---------------- App Runner ----------------
class UKArrivalBuddy(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(VisaScreen(name="visa"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    UKArrivalBuddy().run()