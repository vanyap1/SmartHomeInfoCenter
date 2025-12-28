import kivy
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty, ListProperty, BoundedNumericProperty
kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.stencilview import StencilView
from kivy.uix.togglebutton import ToggleButton

# ...

class analog_meter(Scatter):
    value = NumericProperty(10)
    size_gauge = BoundedNumericProperty(512, min=128, max=512, errorvalue=128)
    def __init__(self, **kwargs):
        super(analog_meter, self).__init__(**kwargs)
        self.bind(value=self._update)
        self._display = Scatter(
            size=(150, 86),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )
        self._needle = Scatter(
            size=(4, 67),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )
        self.lcd_display = Scatter(
            size=(150, 50),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        bg_image = Image(source='images/analog_display_150.png', size=(150, 86), pos=(0, 0))
        _img_needle = Image(source="images/arrow_small.png", size=(4, 134))

        lcd_bg = Image(source='images/lcd_bg.png', size=(150, 44), pos=(0, -47))
        self.pressure_label = Label(text='000', font_name='fonts/lcd.ttf', halign="center",
                                  font_size=36, pos=(25, -76), markup=True)
        self._display.add_widget(bg_image)
        self._needle.add_widget(_img_needle)

        self.lcd_display.add_widget(lcd_bg)
        self.lcd_display.add_widget(self.pressure_label)
        self.add_widget(self._display)
        self.add_widget(self._needle)
        self.add_widget(self.lcd_display)

    def _update(self, *args):
        niddle_angle = 78 - (self.value / 3.8461)
        self._needle.center_x = self._display.center_x
        self._needle.center_y = self._display.center_y - 32
        self._needle.rotation = niddle_angle
        if (self.value <= 160):
            text_color = 'ff0000'
        else:
            text_color = 'ffffff'
        self.pressure_label.text='[color=' + text_color + ']' +str(self.value/100) + ' Bar' + '[/color]'
        pass

class water_tank(Scatter):
    value = NumericProperty(10)

    def __init__(self, **kwargs):
        super(water_tank, self).__init__(**kwargs)
        self.bind(value=self._update)
        self._tank = Scatter(
            size=(110, 135),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )
        water_tank_bar_empty = StencilView(size_hint=(None, None), size=(110, 135), pos=(0, 0))
        water_tank_empty_img = Image(source='images/water_empty.png', size=(110, 135), pos=(0, 0))
        water_tank_bar_empty.add_widget(water_tank_empty_img)
        self._tank.add_widget(water_tank_bar_empty)
        self.water_tank_bar = StencilView(size_hint=(None, None), size=(110, 135), pos=(0, 0))
        water_tank_full_img = Image(source='images/water_full.png', size=(110, 135), pos=(0, 0))
        self.water_tank_bar.add_widget(water_tank_full_img)
        self._tank.add_widget(self.water_tank_bar)
        self.water_tank_bar.height = self.value
        self.percent_lbl=Label(text='100%', font_name='fonts/hemi_head_bd_it.ttf', halign="center", text_size=self.size, font_size=20, pos=(5, 50), markup=True)
        self._tank.add_widget(self.percent_lbl)
        self.add_widget(self._tank)

    def _update(self, *args):
        self.text_color = 'ffffff'
        if (self.value <= 20):
            self.text_color = 'ff0000'
        self.percent_lbl.text='[color='+ self.text_color +']' + str(self.value) + '%[/color]'
        self.water_tank_bar.height = self.value+10


class EnergyResWidget(FloatLayout):  # було: Widget
    fontName = StringProperty("fonts/hemi_head_bd_it.ttf")
    utilityVoltages = ListProperty(["220, 220, 220", "FFFFFF"])
    utilityPower = ListProperty(["2480W", "FFFFFF"])
    batterySoc = ListProperty(["90%", "FFFFFF"])
    batteryStatus = ListProperty(["-1.02A 53.2V 14C", "FFFFFF"])
    pmFrameImage = StringProperty("EN_OK.png")
    analogGaugeValue = NumericProperty(10)
    waterTankValue = NumericProperty(10)
    boilerLedState = BooleanProperty(False)
    boilerSwitchState = BooleanProperty(False)

    def __init__(self, _cb=None, **kwargs):
        super(EnergyResWidget, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.size_hint_y = None
        self.height = 290
        self.pmFrameImage = "EN_OK.png"
        self.analog_display = analog_meter(do_rotation=False, do_scale=False, do_translation=False, value=0, pos=(5, 50))
        self.water_t = water_tank(do_rotation=False, do_scale=False, do_translation=False, value=0, pos=(160, 5))
        self.apicb = _cb
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
                  analogGaugeValue=self._analogMeterUpdate,
                  waterTankValue=self._waterTankUpdate,
                  boilerLedState=self._boilerLedUpdate,
                  boilerSwitchState=self._setBoilerSwitchState
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

        self.boilerLed = Image(source='images/led_off_g.png', size_hint=(None, None), size=(32, 32), pos=(self.x+325, self.y+240))
        self.BoilerLedLabel = Label(
            text="[color=FFFFFF]Boiler[/color]",
            halign="center",
            valign="middle",
            font_size=20, markup=True, font_name="fonts/hemi_head_bd_it.ttf", 
            size_hint=(None, None), size=(80, 30), pos=(self.x+300, self.y+205)
        )

        
        self.swtchBtn = ToggleButton(
            background_normal='images/switch0_off.png', 
            background_down='images/switch0.png',
            border=(0,0,0,0),
            size_hint=(None, None), 
            size=(192/2, 96/2),
            pos=(self.x+295, self.y+150))
        
        self.swtchBtn.bind(state=self._boilerControllSwitch)

        self.widgetLayout.add_widget(self.voltageLabel)   
        self.widgetLayout.add_widget(self.utilityPowerLabel)   
        self.widgetLayout.add_widget(self.batterySocLabel)   
        self.widgetLayout.add_widget(self.batteryStatusLabel)

        self.widgetLayout.add_widget(self.pmFrame)   

        
        self.widgetLayout.add_widget(self.analog_display)
        self.widgetLayout.add_widget(self.water_t)
        self.widgetLayout.add_widget(self.boilerLed)
        self.widgetLayout.add_widget(self.BoilerLedLabel)
        self.widgetLayout.add_widget(self.swtchBtn)

        self.add_widget(self.widgetLayout) 
        
    def _boilerControllSwitch(self, instance, value):
        #WaterHeaterManual = 6
        self.apicb({'switchId': 6, 'state': value == 'down' if True else False})
    
    def _setBoilerSwitchState(self, *args):
        self.swtchBtn.state = 'down' if self.boilerSwitchState else 'normal'
        pass


    def _boilerLedUpdate(self, *args):
        self.boilerLed.source = 'images/led_on_g.png' if self.boilerLedState else 'images/led_off_g.png'
        pass
    
    def _analogMeterUpdate(self, *args):
        self.analog_display.value = self.analogGaugeValue
        pass
    def _waterTankUpdate(self, *args):
        self.water_t.value = self.waterTankValue
        pass

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

            time_widget = EnergyResWidget()
            

            self.LeftPanel.add_widget(time_widget)

            self.dashGroup.add_widget(self.LeftPanel)
          
            
           
            root.add_widget(self.dashGroup)

            def update_time(dt):
                pass

            Clock.schedule_interval(update_time, 1)
            return root

    TestApp().run()