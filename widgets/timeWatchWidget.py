import kivy
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty
kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout
# ...
monthsofyearUA = [
    "Січня", "Лютого", "Березня", "Квітня", "Травня", "Червня",
    "Липня", "Серпня", "Вересня", "Жовтня", "Листопада", "Грудня"
]
daysofweekUA = [
    "Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"
]

class TimeWidget(FloatLayout):  # було: Widget
    size_text = NumericProperty(80)
    fontName = StringProperty("fonts/hemi_head_bd_it.ttf")
    dateFontName = StringProperty("fonts/AdonisC_Bold_Italic.otf")
    timeFontColor = StringProperty("21BCFF")
    dateFontColor = StringProperty("FFFFFF")
    currentTime = ObjectProperty()

    def __init__(self, **kwargs):
        super(TimeWidget, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.size_hint_y = None
        self.height = 120
        self._timeLabelText = ""
        self._dateLabelText = ""
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # фон рухається разом з віджетом
        self.bind(pos=self._update_rect, size=self._update_rect)

        self._timeLabel = Label(
            font_size=self.size_text,
            markup=True,
            font_name=self.fontName,
            halign='left',
            valign='top',
            size_hint=(1, 1),                # заповнює увесь батьківський лейаут
            pos_hint={'x': 0, 'y': 0},
        )
        self._dateLabel = Label(
            font_size=20,
            markup=True,
            font_name=self.dateFontName,
            halign='auto',
            valign='bottom',
            size_hint=(1, None),
            height=30,
            pos_hint={'x': 0, 'y': 0},
 
        )

        self._timeLabel.bind(size=self._timeLabel.setter('text_size'))

        self.add_widget(self._timeLabel)
        self.add_widget(self._dateLabel)
        self.bind(currentTime=self._widgetUpdate)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _widgetUpdate(self, *args):
        self._timeLabelText = self.currentTime.strftime('%H:%M:%S')
        self._dateLabelText = self.currentTime.strftime(    '%d.%m.%Y')
        self._timeLabel.text = f"[color={self.timeFontColor}]{self._timeLabelText}[/color]"
        
        day_idx = self.currentTime.weekday()          # 0=Пн ... 6=Нд
        day_name = daysofweekUA[day_idx]
        month_name = monthsofyearUA[self.currentTime.month - 1].lower()
        d = self.currentTime.day
        y = self.currentTime.year
        if day_idx == 6:
            dow_color = "FF0000"   # Неділя
        elif day_idx == 5:
            dow_color = "FFA500"   # Субота (помаранчевий)
        else:
            dow_color = "FFFFFF"   # Інші
        date_color = self.dateFontColor
        self._dateLabelText = f"{d} {month_name} {y}, "
        self._dateLabel.text = (
            f"[color={date_color}]{self._dateLabelText}[/color]"
            f"[color={dow_color}]{day_name}[/color]"
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