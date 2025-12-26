import kivy
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty
kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout
# ...


class EnergyResWidget(FloatLayout):  # було: Widget
    fontName = StringProperty("fonts/hemi_head_bd_it.ttf")
    

    def __init__(self, **kwargs):
        super(EnergyResWidget, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.size_hint_y = None
        self.height = 290
        
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # фон рухається разом з віджетом
        self.bind(pos=self._update_rect, size=self._update_rect)

        self._timeLabel = Label(
            font_size=16,
            markup=True,
            font_name=self.fontName,
            halign='left',
            valign='top',
            size_hint=(1, 1),                # заповнює увесь батьківський лейаут
            pos_hint={'x': 0, 'y': 0},
        )
        self.add_widget(self._timeLabel)
        

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _widgetUpdate(self, *args):
        pass







if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.image import Image
    from kivy.clock import Clock
    from datetime import datetime

    class TestApp(App):
        def build(self):
            root = FloatLayout()

            self.dashGroup = BoxLayout(
                orientation='horizontal',
                size_hint=(None, None),
                size=(420, 220),   # задайте явний розмір контейнера
                pos=(25, 25),
            )

            self.LeftPanel = BoxLayout(orientation='vertical')

            time_widget = TimeWidget()
            time_widge2 = TimeWidget()
            time_widge3 = TimeWidget()
            time_widge4 = TimeWidget()


            self.LeftPanel.add_widget(time_widget)

            self.dashGroup.add_widget(self.LeftPanel)
          
            
           
            root.add_widget(self.dashGroup)

            def update_time(dt):
                pass

            Clock.schedule_interval(update_time, 1)
            return root

    TestApp().run()