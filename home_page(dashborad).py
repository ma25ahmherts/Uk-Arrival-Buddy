from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget

class ModuleCard(BoxLayout):
    def __init__(self, icon, title, subtitle, priority, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 95
        self.padding = [15, 10]
        self.spacing = 15

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            Color(0.9, 0.9, 0.9, 1)
            self.border = Rectangle(pos=(self.x, self.y), size=(self.width, 1))
        
        self.bind(pos=self.update_bg, size=self.update_bg)

        icon_box = Label(text=icon, font_size=24, size_hint_x=0.18)
        text_layout = BoxLayout(orientation='vertical', spacing=2)
        text_layout.add_widget(Label(text=title, bold=True, color=(0,0,0,1), halign='left', text_size=(200, None), font_size=15))
        text_layout.add_widget(Label(text=subtitle, color=(0.5,0.5,0.5,1), halign='left', text_size=(200, None), font_size=11))

        right_section = BoxLayout(orientation='horizontal', size_hint_x=0.25, spacing=5)
        badge_color = (0.9, 0.1, 0.2, 1) if priority == "Critical" else (0.4, 0.5, 0.6, 1)
        badge = Button(text=priority, size_hint=(None, None), size=(60, 22), 
                       background_normal="", background_color=badge_color, font_size=10, pos_hint={'center_y': 0.5})
        
        right_section.add_widget(badge)
        right_section.add_widget(Label(text=">", color=(0.7, 0.7, 0.7, 1), size_hint_x=None, width=10))

        self.add_widget(icon_box)
        self.add_widget(text_layout)
        self.add_widget(right_section)

    def update_bg(self, instance, value):
        self.bg.pos, self.bg.size = self.pos, self.size
        self.border.pos, self.border.size = self.pos, (self.width, 1)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=110, padding=[20, 15])
        with header.canvas.before:
            Color(0.05, 0.4, 1, 1)
            self.h_rect = Rectangle()
        header.bind(pos=self.update_header, size=self.update_header)
        header.add_widget(Label(text="GB Soul Speak", font_size=26, bold=True, halign='left', text_size=(360, None)))
        header.add_widget(Label(text="Your essential guide to settling in the UK", font_size=13, halign='left', text_size=(360, None)))
        main_layout.add_widget(header)

        # Scroll Content
        scroll = ScrollView(do_scroll_x=False)
        content = BoxLayout(orientation='vertical', size_hint_y=None, padding=[15, 20], spacing=18)
        content.bind(minimum_height=content.setter('height'))

        modules_data = [
            ("🛡️", "UK Rules & Regulations", "Essential compliance info", "Critical"),
            ("✈️", "Airport Arrival & Pickup", "What to do when you land", "High"),
            ("🚆", "Transport Setup", "Oyster cards & travel discounts", "High"),
            ("📱", "SIM Card & Internet", "Get connected to UK networks", "High"),
            ("🏦", "Bank Account & Cards", "Banking and digital options", "Critical"),
            ("🎓", "University Registration", "Complete your enrolment", "High"),
            ("🏥", "GP & Healthcare", "Access NHS support", "High")
        ]
        for icon, title, sub, priority in modules_data:
            content.add_widget(ModuleCard(icon, title, sub, priority))

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        # Nav Bar
        nav = GridLayout(cols=5, size_hint_y=None, height=75)
        with nav.canvas.before:
            Color(1, 1, 1, 1)
            self.n_rect = Rectangle()
        nav.bind(pos=self.update_nav, size=self.update_nav)
        for icon in ["🏠", "🛡️", "✈️", "🚆", "📱"]:
            nav.add_widget(Label(text=icon, font_size=20, color=(0, 0, 0.8, 1)))
        
        main_layout.add_widget(nav)
        self.add_widget(main_layout)

    def update_header(self, instance, value): self.h_rect.pos, self.h_rect.size = instance.pos, instance.size
    def update_nav(self, instance, value): self.n_rect.pos, self.n_rect.size = instance.pos, instance.size