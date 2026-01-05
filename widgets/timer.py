import kivy
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty
kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
# ...


class ElapseTimerWidget(FloatLayout):  # було: Widget
    fontName = StringProperty("fonts/hemi_head_bd_it.ttf")
    dateFontName = StringProperty("fonts/AdonisC_Bold_Italic.otf")
    timeFontColor = StringProperty("21BCFF")
    currentTime = ObjectProperty()
    timerRunning = BooleanProperty(False)
    secondsElapsed = NumericProperty(0)
    minutesElapsed = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ElapseTimerWidget, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.size_hint_y = None
        self.height = 75
        self._timeLabelText = ""
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # фон рухається разом з віджетом
        self.bind(pos=self._update_rect, size=self._update_rect)

        startStopTimerButton = ToggleButton(
            background_normal='images/play.png', 
            background_down='images/stop.png',
            border=(0,0,0,0),
            size_hint=(None, None), 
            size=(75, 75),
        )
        clearTimerButton = Button(
            background_normal='images/clear.png', 
            background_down='images/clear_p.png',
            border=(0,0,0,0),
            size_hint=(None, None), 
            size=(75, 75),
        )
        
        self._timeLabel = Label(
            font_size=40,
            markup=True,
            font_name=self.fontName,
            halign='left',
            valign='top',
            size_hint=(None, None),                # заповнює увесь батьківський лейаут
            size = (400-150, 75),
            pos_hint={'x': 0, 'y': 0},
            text="[color=21BCFF]--:--[/color]",
        )
        
        lay = GridLayout(cols=3, size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        lay.add_widget(startStopTimerButton)
        lay.add_widget(self._timeLabel)
        lay.add_widget(clearTimerButton)
        self.add_widget(lay)



        self._timeLabel.bind(size=self._timeLabel.setter('text_size'))
        clearTimerButton.bind(on_press=self._clearTimer)
        
        self.bind(currentTime=self._widgetUpdate)
        startStopTimerButton.bind(on_press=self._startStopTimer)    

    def _startStopTimer(self, value):
        print(f"Timer button state: {value.state}")
        self.timerRunning = False if value.state == 'normal' else True
    
    def _clearTimer(self, value):
        self.secondsElapsed = 0
        self.minutesElapsed = 0
        self.currentTime = f"{self.minutesElapsed}:{self.secondsElapsed:02d}"
        
    def oneSecondTick(self):
        if self.timerRunning:
            self.secondsElapsed += 1
            if self.secondsElapsed >= 60:
                self.secondsElapsed = 0
                self.minutesElapsed += 1
            
            self.currentTime = f"{self.minutesElapsed}:{self.secondsElapsed:02d}"
            print(f"Timer: {self.minutesElapsed}:{self.secondsElapsed}")


    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _widgetUpdate(self, *args):

        self._timeLabel.text = f"[color={self.timeFontColor}]{self.currentTime}[/color]"
        
        





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