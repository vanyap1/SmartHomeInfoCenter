import kivy
import os
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty, NumericProperty

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation


# --------------------------------------------------
# Віджет з графікою сонячної мережі
# --------------------------------------------------
class RoundedLabel(Label):
    def __init__(self, bg_color=(1, 1, 1, 0.5), radius=10, **kwargs):
        super().__init__(**kwargs)
        
        self.bg_color = bg_color
        self.radius = radius
        
        with self.canvas.before:
            self.bg_color_instruction = Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )
        
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def set_bg_color(self, r, g, b, a):
        """Змінити колір фону"""
        self.bg_color = (r, g, b, a)
        self.bg_color_instruction.rgba = self.bg_color


class SolarGridInfo(FloatLayout):
    acLineConnected = BooleanProperty(True)
    acLineCurrent = NumericProperty(0.0)
    acLinePower = NumericProperty(0.0)
    batPower = NumericProperty(0.0)
    pvPower = NumericProperty(-1)
    batLevel = NumericProperty(100.0)
    batCurrent = NumericProperty(0.0)
    houseLineCurrent = NumericProperty(0.0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, 1)
        self.pos_hint = {'x': 0, 'y': 0}
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.iconsPath = os.path.join(current_dir, "sysInfoImgs") + os.sep
        self.utilityLineIconn = ["dw.d2a791f8.png","dwov.200e3f5a.png"] 
        self.batLevelIcons = ["dc.fd29cdec.png", "dc1.25aeab16.png", "dc2.9602b525.png", "dc3.b9acddc4.png", "dc4.7e4f1a87.png", "dc5.915e0dc1.png", "dc6.52761def.png"]
        
        self.batCurrentDirrectionIcon = {"up":"dcd.40f94616.gif","down":"dcb.d12d17f7.gif"}
        self.houseIcons = {"on": "homeno.73f33990.png", "off": "homehave.62f36967.png"}
        self.inverterIcons = {"on": "dev.c0e77a68.png", "off": "devov.786b73eb.png"}
        self.panelPackIcons = {"left": "sgfov.5ed555f2.png", "right": "bgfov.787884cb.png"}
        self.bind(acLineConnected=self._widgetUpdate,
                  acLineCurrent=self._widgetUpdate,
                  batLevel=self._batLevelUpdate,
                  batCurrent=self._batLevelUpdate,
                  houseLineCurrent=self._houseIconUpdate,
                  acLinePower=self._labelsUpdate,
                  #pvPower=self._labelsUpdate,
                  batPower=self._labelsUpdate,
                  )

        self.houseimg = Image(
            source=self.iconsPath + self.houseIcons["on"],
            size_hint=(0.9, 0.9),
            pos_hint={'x': 0.1, 'y': 0.1},
            allow_stretch=True,
            keep_ratio=True
        )

        self.utilityLine = Image(
            source= self.iconsPath + self.utilityLineIconn[0],
            size_hint=(0.6, 0.6),
            pos_hint={'x': -0.01, 'y': 0.2},
            allow_stretch=True,
            keep_ratio=True
        )

        self.inverrter = Image(
            source=self.iconsPath + self.inverterIcons["on"],
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.515, 'y': 0.43},
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLine_Utility = Image(
            source=self.iconsPath + "dwd.4384250b.gif",
            size_hint=(0.25, 0.25),
            pos_hint={'x': 0.32, 'y': 0.25},
            anim_delay=-1,
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLine_Battery = Image(
            source=self.iconsPath + "dcb.d12d17f7.gif",
            size_hint=(0.15, 0.15),
            pos_hint={'x': 0.4, 'y': 0.44},
            anim_delay=-1,
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLine_Solar = Image(
            source=self.iconsPath + "gdb.30bd45c0.gif",
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.518, 'y': 0.49},
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLineMain= Image(
            source=self.iconsPath + "fzb.247686cc.gif",
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.59, 'y': 0.4},
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True
        )

        self.batteryPack = Image(
            source=self.iconsPath + self.batLevelIcons[0],
            size_hint=(0.2, 0.2),
            pos_hint={'x': 0.31, 'y': 0.43},
            allow_stretch=True,
            keep_ratio=True
        )


        self.panelsPackLeft = Image(
            source=self.iconsPath + self.panelPackIcons["left"],
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.305, 'y': 0.645},
            allow_stretch=True,
            keep_ratio=True
        )

        self.panelsPackRight = Image(
            source=self.iconsPath + self.panelPackIcons["right"],
            size_hint=(0.21, 0.21),
            pos_hint={'x': 0.50, 'y': 0.525},
            allow_stretch=True,
            keep_ratio=True
        )

        self.gridPowerLable = RoundedLabel(
            text='Grid\n1325w',
            bg_color=(1, 1, 1, 0.3),
            radius=20,
            halign='center',
            valign='middle',
            size_hint=(None, None),
            size=(60, 50),
            pos_hint={'x': 0.15, 'y': 0.80}
            )

        self.pvPowerLabel = RoundedLabel(
            text='PV\n2380w',
            bg_color=(1, 1, 1, 0.3),
            radius=20,
            #halign='center',
            #valign='middle',
            size_hint=(None, None),
            size=(60, 50),
            pos_hint={'x': 0.80, 'y': 0.75}
            )
        self.batPowerLabel = RoundedLabel(
            text=' Bat\nsoc:85%\n1800w',
            bg_color=(1, 1, 1, 0.3),
            radius=20,
            halign='center',
            valign='middle',
            size_hint=(None, None),
            size=(70, 60),
            pos_hint={'x': 0.80, 'y': 0.3}
            )

        self.solarStationWidget = FloatLayout(size_hint=(1, 1), pos_hint={'x': -0.1, 'y': 0})
        self.solarStationWidget.add_widget(self.houseimg) 
        self.solarStationWidget.add_widget(self.utilityLine)
        self.solarStationWidget.add_widget(self.powerLine_Utility)
        self.solarStationWidget.add_widget(self.powerLine_Battery)
        self.solarStationWidget.add_widget(self.powerLine_Solar)
        self.solarStationWidget.add_widget(self.inverrter)
        self.solarStationWidget.add_widget(self.batteryPack)
        self.solarStationWidget.add_widget(self.panelsPackLeft)
        self.solarStationWidget.add_widget(self.panelsPackRight)
        self.solarStationWidget.add_widget(self.powerLineMain)
        self.solarStationWidget.add_widget(self.gridPowerLable)
        self.solarStationWidget.add_widget(self.pvPowerLabel)
        self.solarStationWidget.add_widget(self.batPowerLabel)


        self.add_widget(self.solarStationWidget)

    def _labelsUpdate(self, *args):
        self.gridPowerLable.text = f"Grid\n{self.acLinePower}w"
        if self.pvPower >= 0:
            self.pvPowerLabel.text = f"PV\n{self.pvPower}w"
        else:
            self.pvPowerLabel.text = "PV\n--w"
        
        

    def _houseIconUpdate(self, *args):
        if abs(self.houseLineCurrent) > 10:
            new_source = self.iconsPath + self.houseIcons["on"]
            if self.houseimg.source != new_source:
                self.houseimg.source = new_source
        else:
            new_source = self.iconsPath + self.houseIcons["off"]
            if self.houseimg.source != new_source:
                self.houseimg.source = new_source


    def _widgetUpdate(self, *args):
        if self.acLineConnected:
            new_source = self.iconsPath + self.utilityLineIconn[0]
            if self.utilityLine.source != new_source:
                self.utilityLine.source = new_source  # підключено
            
            if abs(self.acLineCurrent) > 50:
                if self.powerLine_Utility.anim_delay != 0.05:
                    self.powerLine_Utility.anim_delay = 0.05  # запустити анімацію
            else:
                if self.powerLine_Utility.anim_delay != -1:
                    self.powerLine_Utility.anim_reset = True
                    self.powerLine_Utility.anim_delay = -1  # зупинити
        else:
            new_source = self.iconsPath + self.utilityLineIconn[1]
            if self.utilityLine.source != new_source:
                self.utilityLine.source = new_source  # відключено
            if self.powerLine_Utility.anim_delay != -1:
                self.powerLine_Utility.anim_reset = True
                self.powerLine_Utility.anim_delay = -1  # зупинити анімацію
        
            


    def _batLevelUpdate(self, *args):
        if 0 <= self.batLevel <= 100:
            if self.batLevel <= 10:
                icon_index = 0
            elif self.batLevel <= 40:
                icon_index = 1
            elif self.batLevel <= 55:
                icon_index = 2
            elif self.batLevel <= 70:
                icon_index = 3
            elif self.batLevel <= 85:
                icon_index = 4
            elif self.batLevel <= 90:
                icon_index = 5
            else:  # 91-100
                icon_index = 6
            
            new_source = self.iconsPath + self.batLevelIcons[icon_index]
            if self.batteryPack.source != new_source:
                self.batteryPack.source = new_source
            self.batPowerLabel.text = f" Bat\nsoc:{int(self.batLevel)}%\n{int(self.batPower)}w"
        
        if self.batCurrent > 2:  # розрядка (позитивний струм)
            new_source = self.iconsPath + self.batCurrentDirrectionIcon["down"]
            if self.powerLine_Battery.source != new_source:
                self.powerLine_Battery.source = new_source
            if self.powerLine_Battery.anim_delay != 0.05:
                self.powerLine_Battery.anim_delay = 0.05
        elif self.batCurrent < -2:  # зарядка (негативний струм)
            new_source = self.iconsPath + self.batCurrentDirrectionIcon["up"]
            if self.powerLine_Battery.source != new_source:
                self.powerLine_Battery.source = new_source
            if self.powerLine_Battery.anim_delay != 0.05:
                self.powerLine_Battery.anim_delay = 0.05
        else:  # струм близький до нуля
            if self.powerLine_Battery.anim_delay != -1:
                self.powerLine_Battery.anim_reset = True
                self.powerLine_Battery.anim_delay = -1
            

class ButtonsBar(FloatLayout):
    def __init__(self, button_callback, **kwargs):
        super().__init__(**kwargs)

        self.button_callback = button_callback
        self.size_hint = (1, None)
        self.pos_hint = {'x': 0, 'y': 0}
        self.buttonsBlock = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=50,
            pos_hint={'x': 0, 'y': 0}
        )

        self.solarSystemInfoBtn = Button(
            text='Solar Info',
            on_release=lambda instance: self.button_callback("1")
        )

        self.graphInfoBtn = Button(
            text='Graph Info',
            on_release=lambda instance: self.button_callback("2")   
        )

        self.buttonsBlock.add_widget(self.solarSystemInfoBtn)
        self.buttonsBlock.add_widget(self.graphInfoBtn)

        self.add_widget(self.buttonsBlock)
    
    def button_callback(self, button_name):
        if(self.button_callback is not None):
            self.button_callback(button_name)


# --------------------------------------------------
# Основний системний віджет
# --------------------------------------------------

class SystemInfoWidget(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # важливо для BoxLayout
        self.size_hint = (1, None)
        self.height = 295

        # фон
        with self.canvas.before:
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

        # графіка
        self.solarPlant = SolarGridInfo()
        self.buttonGroup = ButtonsBar(self.buttons_callback)
        self.add_widget(self.solarPlant)
        self.add_widget(self.buttonGroup)   

        # текст поверх
        self.timeLabel = Label(
            text='[color=21BCFF]--23:45[/color]',
            markup=True,
            font_size=20,
            halign='left',
            valign='top',
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.timeLabel.bind(size=self.timeLabel.setter('text_size'))
        #self.add_widget(self.timeLabel)


    def buttons_callback(self, value):
        print(f"Button pressed: {value}")
        if value == "1":
            if self.solarPlant not in self.children:
                self.solarPlant.opacity = 0  # початкова прозорість
                self.add_widget(self.solarPlant)
                # Анімація появи
                anim = Animation(opacity=1, duration=0.3)
                anim.start(self.solarPlant)
            
        elif value == "2":
            if self.solarPlant in self.children:
                
                anim = Animation(opacity=0, duration=0.3)
                anim.bind(on_complete=lambda *args: self.remove_widget(self.solarPlant))
                anim.start(self.solarPlant)


    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


# --------------------------------------------------
# Тестовий додаток
# --------------------------------------------------

class TestApp(App):
    
    def build(self):
        import random
        root = FloatLayout()

        background = Image(
            source='images/bg_new.png',
            allow_stretch=True,
            keep_ratio=False,
            opacity=0.5,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )

        dashGroup = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(1280, 400),
            pos=(25, 25),
            spacing=10
        )

        leftPanel = BoxLayout(orientation='vertical', size_hint_x=1, size_hint_y=1)
        centerPanel = BoxLayout(orientation='vertical', size_hint_x=1, size_hint_y=1)
        rightPanel = BoxLayout(orientation='vertical', size_hint_x=1, size_hint_y=1)


        self.firsWidget = SystemInfoWidget()
        leftPanel.add_widget(self.firsWidget)
        centerPanel.add_widget(SystemInfoWidget())
        rightPanel.add_widget(SystemInfoWidget())
        
        dashGroup.add_widget(leftPanel)
        dashGroup.add_widget(centerPanel)
        dashGroup.add_widget(rightPanel)
        
        root.add_widget(background)
        root.add_widget(dashGroup)

        self.current = 0
        def update_time(dt):

            state = random.choice([True, False])
            self.current = self.current + 10
            if self.current > 200:
                self.current = 0
            print("AC Line Connected:", state, " Current:", self.current)
            
            
            self.firsWidget.solarPlant.acLineConnected = self.current < 50 or state
            self.firsWidget.solarPlant.acLineCurrent = self.current
            self.firsWidget.solarPlant.batLevel = self.current
            self.firsWidget.solarPlant.batCurrent = -10
            pass

        Clock.schedule_interval(update_time, 1)
        return root


if __name__ == '__main__':
    TestApp().run()
