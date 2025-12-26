

from widgets.timeWatchWidget import TimeWidget
from widgets.weatherWidget import WeatherWidget
from widgets.smartHomeSensors import SmartHomeSensors
from widgets.energyResWidget import EnergyResWidget
from api import SensorApiClient
#
#

if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.image import Image
    from kivy.clock import Clock
    from kivy.uix.image import Image
    from datetime import datetime

    class TestApp(App):
        def build(self):
            root = FloatLayout()
            self.api = SensorApiClient(base_url="http://192.168.1.5:8000")

            #self.dashGroup = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 400), pos=(20, 20))
            self.dashGroup = GridLayout(
                cols=3,
                size_hint=(None, None),
                size=(1280-20, 400-20),   # задайте явний розмір контейнера
                pos=(5, 5),
            )
            self.LeftPanel = BoxLayout(orientation='vertical', padding=5, spacing=5)
            self.CenterPanel = BoxLayout(orientation='vertical', padding=5, spacing=5)
            self.RightPanel = BoxLayout(orientation='vertical', padding=5, spacing=5)   

            time_widget = TimeWidget()
            weather_widget = WeatherWidget()
            smartHomeSensors_widget = SmartHomeSensors()
            energyResWidget_widget = EnergyResWidget()


            self.LeftPanel.add_widget(time_widget)
            self.LeftPanel.add_widget(weather_widget)

            self.CenterPanel.add_widget(smartHomeSensors_widget)
            self.CenterPanel.add_widget(energyResWidget_widget)

            self.dashGroup.add_widget(self.LeftPanel)
            self.dashGroup.add_widget(self.CenterPanel)
            self.dashGroup.add_widget(self.RightPanel)
                       
            self.background_image = Image(source='images/bg_new.png', opacity=0.5, allow_stretch=True, keep_ratio=False)
            root.add_widget(self.background_image)
            root.add_widget(self.dashGroup)
            #weather_widget._widgetUpdate()



            def update_time(dt):
                time_widget.currentTime = datetime.now()
                res = self.api.get_channel("Battery:0x0003", 5)
                res.append("FFFFFF")
                smartHomeSensors_widget.line1 = res

                res = self.api.get_channel("Gateway:0x0001", 3)
                res.append("21BCFF")
                smartHomeSensors_widget.line2 = res

                oldServData = self.api.oldApiGetData().split('/')
                #['###2025', '12', '26', '5', '16', '47', '17', 'n', '-1.1', '51.3', '0', '26.3', '26.3', 'th', 'tl', '___', '0', '^-^', '376', '227', '1']
                res = ['Вулиця:', oldServData[8], '°C', 'FFFFFF']
                smartHomeSensors_widget.line3 = res
                
                smartHomeSensors_widget.line4 = ['---:', "---", '%', '21BCFF']
                smartHomeSensors_widget.line5 = ['---:', "---", '%', '21BCFF']


            def weather_update(dt):
                weather_widget._widgetUpdate()


            Clock.schedule_interval(update_time, 5)
            Clock.schedule_interval(weather_update, 60)
            return root

    TestApp().run()






