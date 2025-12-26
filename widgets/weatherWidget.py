import kivy
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ObjectProperty
import requests


kivy.require('1.6.0')

from kivy.uix.floatlayout import FloatLayout
iconsPath = "widgets/weatherIcons/"
weatherServerAPI_URL = "http://wttr.in/Svalyava?format=j1&lang=ru"
WWO_CODE = {
    # Clear / Cloud
    "113": "wic_clear_d.png",          # Clear/Sunny
    "116": "wic_cloudy.png",           # Partly Cloudy
    "119": "wic_cloudy.png",           # Cloudy
    "122": "wic_rp_big_cloudy.png",    # Overcast

    # Mist / Fog / Haze
    "143": "wic_rp_fog_mist.png",      # Mist
    "248": "wic_rp_fog_mist.png",      # Fog
    "260": "wic_rp_fog_mist.png",      # Freezing fog

    # Patchy rain / drizzle
    "176": "wic_rain.png",             # Patchy rain nearby
    "263": "wic_drizzle.png",          # Patchy light drizzle
    "266": "wic_drizzle.png",          # Light drizzle
    "281": "wic_sleet.png",            # Freezing drizzle
    "284": "wic_sleet.png",            # Heavy freezing drizzle

    # Rain
    "293": "wic_rain.png",             # Patchy light rain
    "296": "wic_rain.png",             # Light rain
    "299": "wic_rp_big_rain.png",      # Moderate rain at times
    "302": "wic_rain.png",             # Moderate rain
    "305": "wic_rp_big_rain.png",      # Heavy rain at times
    "308": "wic_rp_big_rain.png",      # Heavy rain

    # Freezing rain / Sleet
    "311": "wic_rp_sleet.png",         # Light freezing rain
    "314": "wic_rp_sleet.png",         # Moderate/Heavy freezing rain
    "317": "wic_rp_sleet.png",         # Light sleet
    "320": "wic_rp_sleet.png",         # Moderate/Heavy sleet
    "182": "wic_sleet.png",            # Patchy sleet nearby
    "185": "wic_sleet.png",            # Patchy freezing drizzle nearby
    "350": "wic_hail.png",             # Ice pellets

    # Snow
    "323": "wic_snow.png",             # Patchy light snow
    "326": "wic_snow.png",             # Light snow
    "329": "wic_snow.png",             # Moderate snow at times
    "332": "wic_snow.png",             # Moderate snow
    "335": "wic_rp_snow.png",          # Heavy snow
    "338": "wic_rp_snow.png",          # Heavy snow
    "227": "wic_snow.png",             # Blowing snow
    "230": "wic_rp_snow.png",          # Blizzard

    # Showers
    "353": "wic_rain.png",             # Light rain shower
    "356": "wic_rp_big_rain.png",      # Moderate/Heavy rain shower
    "359": "wic_rp_big_rain.png",      # Torrential rain shower
    "362": "wic_rp_sleet.png",         # Light sleet showers
    "365": "wic_rp_sleet.png",         # Moderate/Heavy sleet showers
    "368": "wic_snow.png",             # Light snow showers
    "371": "wic_rp_snow.png",          # Moderate/Heavy snow showers
    "374": "wic_hail.png",             # Light showers of ice pellets
    "377": "wic_hail.png",             # Moderate/Heavy showers of ice pellets

    # Thunder
    "200": "wic_thunder.png",          # Thundery outbreaks nearby
    "386": "wic_rp_thunder.png",       # Patchy light rain with thunder
    "389": "wic_rp_storm.png",         # Moderate/Heavy rain with thunder
    "392": "wic_rp_thunder.png",       # Patchy light snow with thunder
    "395": "wic_rp_thunder.png",       # Moderate/Heavy snow with thunder
}

class WeatherWidget(FloatLayout): 
    currentWeatherCondition = StringProperty("Sunny \n 25°C \n Humidity: 40% \n Дані відсутні")
    currentWeatherIcon = StringProperty(iconsPath + WWO_CODE["113"])
    partsOfDayIcons = ObjectProperty([iconsPath + WWO_CODE["113"], iconsPath + WWO_CODE["116"], iconsPath + WWO_CODE["119"], iconsPath + WWO_CODE["122"]])  # список іконок для частин дня
    partsOfDayLabels = ObjectProperty(["+25°C\n Humidity: 40%", "+22°C\n Humidity: 50%", "+20°C\n Humidity: 60%", "+18°C\n Humidity: 70%"])  # список підписів для частин дня
    def __init__(self, **kwargs):
        super(WeatherWidget, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.size_hint_y = None
        self.height = 250
        self.padding = 10
        self.spacing = 10
        
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.5)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # фон рухається разом з віджетом
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        
        self.topPanel = GridLayout(cols=2, size_hint=(1, None), height=120)
        
        self.mainIcon = Image(source=self.currentWeatherIcon, size_hint=(None, None), size=(120, 120), width=120)
        self.currentWeatherLabel = Label(
            text=self.currentWeatherCondition,
            font_size=18,
            markup=True,
            #font_name=self.dateFontName,
            halign='left',
            valign='middle',
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},   
        )

        
        self.topPanel.add_widget(self.mainIcon)
        self.topPanel.add_widget(self.currentWeatherLabel)


        self.bottomPanel = GridLayout(cols=4, size_hint=(1, None), height=270/2)
        self._dayPartIcon1 = image = Image(source=self.partsOfDayIcons[0], size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self._dayPartIcon2 = image = Image(source=self.partsOfDayIcons[1], size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self._dayPartIcon3 = image = Image(source=self.partsOfDayIcons[2], size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self._dayPartIcon4 = image = Image(source=self.partsOfDayIcons[3], size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.bottomPanel.add_widget(self._dayPartIcon1)
        self.bottomPanel.add_widget(self._dayPartIcon2)
        self.bottomPanel.add_widget(self._dayPartIcon3)
        self.bottomPanel.add_widget(self._dayPartIcon4)
        

        self._dayPartLabel1 = Label(text=self.partsOfDayLabels[0], font_size=14, halign='center', valign='top', size_hint=(1, None), height=30)
        self._dayPartLabel2 = Label(text=self.partsOfDayLabels[1], font_size=14, halign='center', valign='top', size_hint=(1, None), height=30)
        self._dayPartLabel3 = Label(text=self.partsOfDayLabels[2], font_size=14, halign='center', valign='top', size_hint=(1, None), height=30)
        self._dayPartLabel4 = Label(text=self.partsOfDayLabels[3], font_size=14, halign='center', valign='top', size_hint=(1, None), height=30)
        self.bottomPanel.add_widget(self._dayPartLabel1)
        self.bottomPanel.add_widget(self._dayPartLabel2)
        self.bottomPanel.add_widget(self._dayPartLabel3)
        self.bottomPanel.add_widget(self._dayPartLabel4)


        self.rootLayout = BoxLayout(orientation='vertical', size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.rootLayout.add_widget(self.topPanel)
        self.rootLayout.add_widget(self.bottomPanel)
        self.add_widget(self.rootLayout)


        
        self._currentWeatherLabel = Label(
            font_size=20,
            markup=True,
            #font_name=self.dateFontName,
            halign='auto',
            valign='bottom',
            size_hint=(1, None),
            height=30,
            pos_hint={'x': 0, 'y': 0},
 
        ) 
    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _widgetUpdate(self, *args):
        try:
            response = requests.get(weatherServerAPI_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Failed to fetch weather data: {e}")
            return
    # Поточні умови
        try:
            cur = data['current_condition'][0]
            tempC = cur.get('temp_C') or cur.get('tempC')
            vis = cur.get('visibility')
            wind = cur.get('windspeedKmph')
            hum = cur.get('humidity')
            code = str(cur.get('weatherCode'))
        # Опис (RU, бо lang=ru; є також 'weatherDesc')
            if cur.get('lang_ru'):
                desc = cur['lang_ru'][0].get('value')
            else:
                desc = (cur.get('weatherDesc') or [{}])[0].get('value')

            icon_file = WWO_CODE.get(code)
            if icon_file:
                self.mainIcon.source = iconsPath + icon_file

        # Оновити текст поточної погоди (можете підлаштувати формат)
            self.currentWeatherLabel.text = (
                f"{desc or ''}\n"
                f"Темп: {tempC}°C  Вологість: {hum}%\n"
                f"Вітер: {wind} км/год  Видимість: {vis} км"
            )
        except Exception as e:
            print(f"Parse current_condition error: {e}")

    # Прогноз на завтра (слоти 3,4,6,7)
        try:
            hours = data['weather'][1]['hourly']
            slot_indices = [3, 4, 6, 7]
            icons = [self._dayPartIcon1, self._dayPartIcon2, self._dayPartIcon3, self._dayPartIcon4]
            labels = [self._dayPartLabel1, self._dayPartLabel2, self._dayPartLabel3, self._dayPartLabel4]

            for i, idx in enumerate(slot_indices):
                if idx < len(hours):
                    h = hours[idx]
                    t = h.get('tempC') or h.get('temp_C')
                    hum = h.get('humidity')
                    code = str(h.get('weatherCode'))
                    icon_file = WWO_CODE.get(code)
                    if icon_file:
                        icons[i].source = iconsPath + icon_file
                    labels[i].text = f"{t}°C\nHum: {hum}%"
        except Exception as e:
            print(f"Parse forecast error: {e}")







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

            weather_widget = WeatherWidget()
            

            self.LeftPanel.add_widget(weather_widget)
            self.dashGroup.add_widget(self.LeftPanel)
            
            root.add_widget(self.dashGroup)

            def update_time(dt):
                now = datetime.now()
                

            Clock.schedule_interval(update_time, 15)
            return root

    TestApp().run()