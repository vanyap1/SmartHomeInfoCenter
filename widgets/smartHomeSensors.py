import kivy
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout



class SmartHomeSensors(FloatLayout):
    fontName = StringProperty("fonts/AdonisC_Bold_Italic.otf")

    line1 = ListProperty(["Двір:", "22",  "°C", "FFFFFF"])
    line2 = ListProperty(["Дитяча:", "45",  "%", "21BCFF"])
    line3 = ListProperty(["Коридор:", "22",  "°C", "FFFFFF"])
    line4 = ListProperty(["Бойлер:", "23",  "°C", "FFFFFF"])
    line5 = ListProperty(["Котел:", "24",  "°C", "FFFFFF"])

    def __init__(self, **kwargs):
        super(SmartHomeSensors, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.size_hint_y = None
        self.height = 80

        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

        # Підписка на зміни властивостей
        self.bind(line1=self._widgetUpdate,
                  line2=self._widgetUpdate,
                  line3=self._widgetUpdate,
                  line4=self._widgetUpdate,
                  line5=self._widgetUpdate)

        self.widgetGrig = GridLayout(cols=3, size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.widgetIcon1 = Image(source='images/OutdoorTemp.png', size_hint_x=None, width=70)
        self.widgetLabel = Label(
            text="[color=21BCFF][b]Outdoor Temp:[/b][/color]\n[color=FFFFFF]22 °C[/color]",
            font_size=18, markup=True, font_name=self.fontName, 
        )
        self.widgetGrig.add_widget(self.widgetIcon1)
        self.widgetGrig.add_widget(self.widgetLabel)
        self.widgetGrig.add_widget(label:=Label())  # Порожній віджет для вирівнювання
        
        self.add_widget(self.widgetGrig)

        # Ініціалізація тексту
        self._widgetUpdate()

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _widgetUpdate(self, *args):
        # Використовуємо line1; за потреби додайте окремі лейбли для line2..line4
        self.widgetLabel.text = (
            f"[b]{self.line1[0]}[/b] [color={self.line1[3]}]{self.line1[1]} {self.line1[2]}[/color]"
            f"\n[b]{self.line2[0]}[/b] [color={self.line2[3]}]{self.line2[1]} {self.line2[2]}[/color]"
            f"\n[b]{self.line3[0]}[/b] [color={self.line3[3]}]{self.line3[1]} {self.line3[2]}[/color]"
            f"\n[b]{self.line4[0]}[/b] [color={self.line4[3]}]{self.line4[1]} {self.line4[2]}[/color]"
            #f"\n[b]{self.line5[0]}[/b] [color={self.line5[3]}]{self.line5[1]} {self.line5[2]}[/color]"
        )







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
            #self.LeftPanel2 = BoxLayout(orientation='vertical', size_hint=(None, None), size=(400, 200))

            time_widget = TimeWidget()
            time_widge2 = TimeWidget()
            time_widge3 = TimeWidget()
            time_widge4 = TimeWidget()

        # опціонально: чіткі висоти для стеку
        # time_widget.size_hint_y = None; time_widget.height = 100
        # time_widge2.size_hint_y = None; time_widge2.height = 100
        # або порівну:
        # time_widget.size_hint_y = 0.5
        # time_widge2.size_hint_y = 0.5

            self.LeftPanel.add_widget(time_widget)
            #self.LeftPanel.add_widget(time_widge2)

            #self.LeftPanel2.add_widget(time_widge3)
            #self.LeftPanel2.add_widget(time_widge4)


            self.dashGroup.add_widget(self.LeftPanel)
            #self.dashGroup.add_widget(self.LeftPanel2)
            
           
            root.add_widget(self.dashGroup)

            def update_time(dt):
                now = datetime.now()
                time_widget.currentTime = now
                time_widge2.currentTime = now
                time_widge3.currentTime = now
                time_widge4.currentTime = datetime.strptime("15:45:30", "%H:%M:%S")

            Clock.schedule_interval(update_time, 1)
            return root

    TestApp().run()