import kivy
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty, ListProperty
kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
# ...


class EnergyResWidget(FloatLayout):  # було: Widget
    fontName = StringProperty("fonts/hemi_head_bd_it.ttf")
    utilityVoltages = ListProperty(["220, 220, 220", "FFFFFF"])
    utilityPower = ListProperty(["2480W", "FFFFFF"])
    batterySoc = ListProperty(["90%", "FFFFFF"])
    batteryStatus = ListProperty(["-1.02A 53.2V 14C", "FFFFFF"])
    pmFrameImage = StringProperty("EN_OK.png")
    def __init__(self, **kwargs):
        super(EnergyResWidget, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.size_hint_y = None
        self.height = 290
        self.pmFrameImage = "EN_OK.png"


        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # фон рухається разом з віджетом
        self.bind(pos=self._update_rect, size=self._update_rect)

        self.widgetLayout = Scatter(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.bind(utilityVoltages=self._energyMonitorUpdate,
                  utilityPower=self._energyMonitorUpdate,
                  batterySoc=self._energyMonitorUpdate,
                  batteryStatus=self._energyMonitorUpdate,
                  pmFrameImage=self._energyMonitorUpdate,
                  )
        print(self.size)
        self.pmFrame = Image(source=f"images/{self.pmFrameImage}", size_hint=(None, None), size=(286, 138), pos=(self.x+5, self.y+145))
        self.voltageLabel = Label(
            #color=(0.1, 0.1, 1, 1),
            halign="center",
            valign="middle",
            font_size=30, markup=True, font_name="fonts/lcd.ttf", 
            size_hint=(None, None), size=(210, 30), pos=(self.x+50, self.y+250)
        )
        self.utilityPowerLabel = Label(
            halign="center",
            #color=(0.1, 1, 0.1, 1),
            valign="middle",
            font_size=30, markup=True, font_name="fonts/lcd.ttf", 
            size_hint=(None, None), size=(210, 30), pos=(self.x+50, self.y+220)
        )
        self.batterySocLabel = Label(
            #color=(1, 1, 0.1, 1),
            halign="center",
            valign="middle",
            font_size=30, markup=True, font_name="fonts/lcd.ttf", 
            size_hint=(None, None), size=(210, 30), pos=(self.x+50, self.y+190)
        )
        self.batteryStatusLabel = Label(
            #color=(1, 1, 0.1, 1),
            halign="center",
            valign="middle",
            font_size=30, markup=True, font_name="fonts/lcd.ttf", 
            size_hint=(None, None), size=(210, 30), pos=(self.x+50, self.y+160)
        )
        
        self.widgetLayout.add_widget(self.voltageLabel)   
        self.widgetLayout.add_widget(self.utilityPowerLabel)   
        self.widgetLayout.add_widget(self.batterySocLabel)   
        self.widgetLayout.add_widget(self.batteryStatusLabel)

        self.widgetLayout.add_widget(self.pmFrame)   

        self.add_widget(self.widgetLayout) 
        

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _energyMonitorUpdate(self, *args):
        self.pmFrame.source = f"images/{self.pmFrameImage}"
        self.voltageLabel.text = "[color=" + self.utilityVoltages[1] + "]" + self.utilityVoltages[0] + "[/color]"
        self.utilityPowerLabel.text = "[color=" + self.utilityPower[1] + "]" + self.utilityPower[0] + "[/color]"
        self.batterySocLabel.text = "[color=" + self.batterySoc[1] + "]" + self.batterySoc[0] + "[/color]"
        self.batteryStatusLabel.text = "[color=" + self.batteryStatus[1] + "]" + self.batteryStatus[0] + "[/color]"
        pass

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