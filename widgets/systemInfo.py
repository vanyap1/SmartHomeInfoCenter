import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


# --------------------------------------------------
# Віджет з графікою сонячної мережі
# --------------------------------------------------

class SolarGridInfo(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, 1)
        self.pos_hint = {'x': 0, 'y': 0}

        self.houseimg = Image(
            source='widgets/sysInfoImgs/homehave.62f36967.png',
            size_hint=(0.9, 0.9),
            pos_hint={'x': 0.1, 'y': 0.1},
            allow_stretch=True,
            keep_ratio=True
        )

        self.utilityLine = Image(
            source='widgets/sysInfoImgs/dw.d2a791f8.png',
            size_hint=(0.6, 0.6),
            pos_hint={'x': -0.01, 'y': 0.2},
            allow_stretch=True,
            keep_ratio=True
        )

        self.inverrter = Image(
            source='widgets/sysInfoImgs/dev.c0e77a68.png',
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.515, 'y': 0.43},
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLine_Utility = Image(
            source='widgets/sysInfoImgs/dwd.4384250b.gif',
            size_hint=(0.25, 0.25),
            pos_hint={'x': 0.32, 'y': 0.25},
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLine_Battery = Image(
            source='widgets/sysInfoImgs/dcb.d12d17f7.gif',
            size_hint=(0.15, 0.15),
            pos_hint={'x': 0.4, 'y': 0.44},
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLine_Solar = Image(
            source='widgets/sysInfoImgs/gdb.30bd45c0.gif',
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.518, 'y': 0.49},
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True
        )

        self.powerLineMain= Image(
            source='widgets/sysInfoImgs/fzb.247686cc.gif',
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.59, 'y': 0.4},
            anim_delay=0.05,
            allow_stretch=True,
            keep_ratio=True
        )

        self.batteryPack = Image(
            source='widgets/sysInfoImgs/dc5.915e0dc1.png',
            size_hint=(0.2, 0.2),
            pos_hint={'x': 0.31, 'y': 0.43},
            allow_stretch=True,
            keep_ratio=True
        )


        self.panelsPackLeft = Image(
            source='widgets/sysInfoImgs/sgfov.5ed555f2.png',
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.305, 'y': 0.645},
            allow_stretch=True,
            keep_ratio=True
        )

        self.panelsPackRight = Image(
            source='widgets/sysInfoImgs/bgfov.787884cb.png',
            size_hint=(0.21, 0.21),
            pos_hint={'x': 0.50, 'y': 0.525},
            allow_stretch=True,
            keep_ratio=True
        )


        self.add_widget(self.houseimg) 
        self.add_widget(self.utilityLine)
        self.add_widget(self.powerLine_Utility)
        self.add_widget(self.powerLine_Battery)
        self.add_widget(self.powerLine_Solar)

        self.add_widget(self.inverrter)
        self.add_widget(self.batteryPack)
        self.add_widget(self.panelsPackLeft)
        self.add_widget(self.panelsPackRight)
        self.add_widget(self.powerLineMain)

        

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
        self.add_widget(self.solarPlant)

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

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


# --------------------------------------------------
# Тестовий додаток
# --------------------------------------------------

class TestApp(App):

    def build(self):
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

        leftPanel.add_widget(SystemInfoWidget())
        centerPanel.add_widget(SystemInfoWidget())
        rightPanel.add_widget(SystemInfoWidget())

        dashGroup.add_widget(leftPanel)
        dashGroup.add_widget(centerPanel)
        dashGroup.add_widget(rightPanel)

        root.add_widget(background)
        root.add_widget(dashGroup)

        return root


if __name__ == '__main__':
    TestApp().run()
