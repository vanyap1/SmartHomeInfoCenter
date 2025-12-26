from widgets.timeWatchWidget import TimeWidget
from widgets.weatherWidget import WeatherWidget
from widgets.smartHomeSensors import SmartHomeSensors
from widgets.energyResWidget import EnergyResWidget
from api import SensorApiClient

from udpService import UdpAsyncClient
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
            self.energySrc="NONE"
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


            self.count = 0
            def update_time(dt):
                time_widget.currentTime = datetime.now()
                if(self.energySrc == "AC"):
                    energyResWidget_widget.pmFrameImage = 'EN_OK.png'
                elif(self.energySrc == "err"):
                    energyResWidget_widget.pmFrameImage = 'EN_ERR.png'    
                else:
                    energyResWidget_widget.pmFrameImage = 'EN_NOK.png' 
                
               
            
            def weather_update(dt):
                weather_widget._widgetUpdate()
                res = self.api.get_channel("Battery:0x0003", 5)
                res.append("FFFFFF")
                smartHomeSensors_widget.line1 = res

                res = self.api.get_channel("Gateway:0x0001", 3)
                res.append("21BCFF")
                smartHomeSensors_widget.line2 = res
                try:
                    self.waterTankLevel = self.api.get_channel("WaterTank:0x0001", 1)[1]
                    self.waterTankPressure = self.api.get_channel("WaterTank:0x0001", 2)[1]
                    self.waterTankLevel = float(self.waterTankLevel)
                    self.waterTankPressure = float(self.waterTankPressure)*100
                except:
                    self.waterTankLevel = 1
                    self.waterTankPressure = 0
                    pass
               
                try:
                    oldServData = self.api.oldApiGetData().split('/')
                #['###2025', '12', '26', '5', '16', '47', '17', 'n', '-1.1', '51.3', '0', '26.3', '26.3', 'th', 'tl', '___', '0', '^-^', '376', '227', '1']
                    res = ['Вулиця:', oldServData[8], '°C', 'FFFFFF']
                    smartHomeSensors_widget.line3 = res
                    
                    energyResWidget_widget.analogGaugeValue = self.waterTankPressure
                    energyResWidget_widget.waterTankValue = self.waterTankLevel
                
                    smartHomeSensors_widget.line4 = ['---:', "---", '%', '21BCFF']
                    smartHomeSensors_widget.line5 = ['---:', "---", '%', '21BCFF']
                except Exception as e:
                    print(f"Error parsing old API data: {e}")

            def serverUdpIncomingData(data):
                
                try:
                    energyResWidget_widget.utilityVoltages = [str(data['voltage']).replace("[", "").replace("]", "") + " V", "FFFFFF"]
                    energyResWidget_widget.utilityPower = [f"{data['total_power']} W", "FFFFFF"]
                    self.energySrc = data['source']
                except:
                    self.energySrc = "err"
                    energyResWidget_widget.utilityVoltages = ["ERROR", "FF0000"]
                    energyResWidget_widget.utilityPower = ["ERROR", "FF0000"]
                    pass
        
            def batteryUdpIncomingData(data):
                socLevelColor = "00ff00"
                socCurrentColor = "20ff20"
                try:
                    pass
                    if(data['socStatusLoad'][0] <= 80):
                        socLevelColor = "ffff00"
                    if(data['socStatusLoad'][0] <= 60):
                        socLevelColor = "ff0000"

                    if((data['socCurrent']/10) <= -1):
                        socCurrentColor = "ffff00"
                    if((data['socCurrent']/10) >= 1):
                        socCurrentColor = "8080ff"
                    energyResWidget_widget.batterySoc = [f"{data['socStatusLoad'][0]} %", socLevelColor]
                    energyResWidget_widget.batteryStatus = [f"{data['socCurrent']/10}A {data['socVoltage']/100} V {int(data['socTemperature']/10)}C", socCurrentColor]
                except:
                    energyResWidget_widget.batterySoc = ["ERROR", "FF0000"]
                    energyResWidget_widget.batteryStatus = ["ERROR", "FF0000"]
                    pass

            Clock.schedule_interval(update_time, 1)
            Clock.schedule_interval(weather_update, 60)
            self.udpClient = UdpAsyncClient(self, serverUdpIncomingData, 5005)
            self.udpClient = UdpAsyncClient(self, batteryUdpIncomingData, 5006)

            return root

    TestApp().run()






