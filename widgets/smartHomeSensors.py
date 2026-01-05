import kivy
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle

class RoundedLabel(Label):
    def __init__(self, bg_color=(1, 1, 1, 0.5), radius=10, **kwargs):
        super().__init__(**kwargs)
        
        self.radius = radius
        self.bg_color = bg_color
        
        with self.canvas.before:
            self.bg_color_instruction = Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )
        
        self.bind(pos=self._update_rect, 
                size=self._update_rect,
                )
    
    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def set_bg_color(self, r, g, b, a):
        """Змінити колір фону"""
        self.bg_color = (r, g, b, a)
        self.bg_color_instruction.rgba = self.bg_color


class SmartHomeSensors(FloatLayout):
    fontName = StringProperty("fonts/AdonisC_Bold_Italic.otf")

    line1 = ListProperty(["Двір:", "22",  "°C", "FFFFFF"])
    line2 = ListProperty(["Дитяча:", "45",  "%", "21BCFF"])
    line3 = ListProperty(["Коридор:", "22",  "°C", "FFFFFF"])
    outdoorTemp = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(SmartHomeSensors, self).__init__(**kwargs)
        self.size_hint = (1, 1)
        self.pos_hint = {'x': 0, 'y': 0}

        

        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

        # Підписка на зміни властивостей
        self.bind(line1=self._label1Update,
                  line2=self._label2Update,
                  line3=self._label3Update,
                  outdoorTemp=self._tempUpdate
                  )

        ##self.widgetGrig = GridLayout(cols=3, size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}, padding=5, spacing=5)
        
        
        self.widgetIcon1 = Image(source='images/OutdoorTemp.png',
                                 pos_hint={'x': -.32, 'y': 0.1},
                                 size_hint=(0.8, 0.8),
                                 allow_stretch=True,
                                 keep_ratio=True)
        
        self.widgetLabel1 = Label(
            text="-- -- --",
            pos_hint={'x': 0.3, 'y': 0.1},
            size_hint=(None, None),
            size=(300, 20),
            text_size=(300, None),
            halign='left',
            valign='middle',
            font_size=18, markup=True, font_name=self.fontName, 
        )
        self.widgetLabel2 = Label(
            text="-- -- --",
            pos_hint={'x': 0.3, 'y': 0.1},
            size_hint=(None, None),
            size=(300, 20),
            text_size=(300, None),
            halign='left',
            valign='middle',
            font_size=18, markup=True, font_name=self.fontName, 
        )
        self.widgetLabel3 = Label(
            text="-- -- --",
            pos_hint={'x': 0.3, 'y': 0.1},
            size_hint=(None, None),
            size=(300, 20),
            text_size=(300, None),
            halign='left',
            valign='middle',
            font_size=18, markup=True, font_name=self.fontName, 
        )

        self.outdoorTermometer = RoundedLabel(
            text="-10.1°C",
            font_size=32, markup=True, 
            font_name=self.fontName,
            bg_color= (0, 0, 0, 0.7), 
            radius=10,
            halign='center',
            valign='middle',
            size_hint=(None, None),
            size=(120, 66),
            pos_hint={'x': 0.69, 'y': 0.05}
        )


        self.add_widget(self.widgetIcon1)
        self.labelsBox = GridLayout(cols=1, size_hint=(None, 1), pos_hint={'x': 0.16, 'y': -0.05}, spacing=0)
        self.labelsBox.add_widget(self.widgetLabel1)
        self.labelsBox.add_widget(self.widgetLabel2)
        self.labelsBox.add_widget(self.widgetLabel3)
        self.add_widget(self.labelsBox)
        self.add_widget(self.outdoorTermometer)  # Порожній віджет для вирівнювання
        
        #self.add_widget(self.widgetGrig)

        # Ініціалізація тексту
        
        

    def _tempUpdate(self, instance, value):
        self.outdoorTermometer.text = f"{value:.1f}°C"
        print(f"Outdoor Temp updated to: {value:.1f}°C")
        if value < 0:
            print("Setting background color for below 0°C")
            self.outdoorTermometer.set_bg_color(0, 0, 0.5, 0.7)  # Темно-синій для від'ємних температур
        elif 0 <= value < 15:
            self.outdoorTermometer.set_bg_color(0, 0.5, 1, 0.7)  # Світло-синій для холодних температур
        elif 15 <= value < 25:
            self.outdoorTermometer.set_bg_color(0, 1, 0, 0.7)  # Зелений для комфортних температур
        elif 25 <= value < 35:
            self.outdoorTermometer.set_bg_color(1, 0.5, 0, 0.7)  # Помаранчевий для теплих температур
        else:
            self.outdoorTermometer.set_bg_color(1, 0, 0, 0.7)  # Червоний для спекотних температур

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _label1Update(self, *args):
        self.widgetLabel1.text = (f"[b]{self.line1[0]}[/b] [color={self.line1[3]}]{self.line1[1]} {self.line1[2]}[/color]")
    def _label2Update(self, *args):
        self.widgetLabel2.text = (f"[b]{self.line2[0]}[/b] [color={self.line2[3]}]{self.line2[1]} {self.line2[2]}[/color]")
    def _label3Update(self, *args):
        self.widgetLabel3.text = (f"[b]{self.line3[0]}[/b] [color={self.line3[3]}]{self.line3[1]} {self.line3[2]}[/color]")


    






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