#import kivy
#kivy.require('1.0.6')
#from glob import glob
#from os.path import join, dirname
#from kivy.app import App
#from kivy.logger import Logger
#from kivy.uix.scatter import Scatter
#from kivy.properties import StringProperty, ObjectProperty
#import sys
import subprocess
import time
#import random
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen , ScreenManager
from threading import Thread
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
#from kivy.uix.gridlayout import GridLayout
#from kivy.animation import Animation
from kivy.uix.image import Image
#from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
#from kivy.uix.progressbar import ProgressBar
#from kivy.properties import NumericProperty
#from kivy.properties import BoundedNumericProperty
from kivy.properties import StringProperty

#import custom_fun
import io , os, re, smbus # , i2c , psutil
#from kivy.uix.videoplayer import VideoPlayer
#from kivy_garden import graph
#import configparser
#import struct
from kivy.core.window import Window
from kivy.animation import Animation
#from math import sin
from kivy_garden.graph import Graph, MeshLinePlot, LinePlot, SmoothLinePlot
from kivy.factory import Factory
Builder.load_file('kv/wet_widget.kv')
Builder.load_file('kv/SmartHomeWidget.kv')

shell_str=subprocess.check_output(["lscpu | grep 'Model name' | cut -f 2 -d ':' | awk '{$1=$1}1'"] , shell=True)
shell_str=shell_str.decode('utf-8')
if shell_str!='Cortex-A7':
    Window.size = (1280,400)

class SmartHomeDataWidget(Screen):

    pass

class WetherWidged(Screen):
    CurrentWet = StringProperty("Температура:    +31С \nВидимість:          10Км\nМісцями дощ \nВітер:                 10Км/г")
    CurrentWetIcon = StringProperty('WetIcons/wic_snow_n.png')
    Tommorow1 = StringProperty('WetIcons/wic_snow_n.png')
    Tommorow2 = StringProperty('WetIcons/wic_rp_big_rain.png')
    Tommorow3 = StringProperty('WetIcons/wic_thunder.png')
    Tommorow4 = StringProperty('WetIcons/wic_clear_d.png')

    TommorowT1 = StringProperty('+33(34) °C ')
    TommorowT2 = StringProperty('+24(26) °C ')
    TommorowT3 = StringProperty('26 °C ')
    TommorowT4 = StringProperty(shell_str)
    pass





class Dashboard(FloatLayout):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.background_image = Image(source='images/bg.png', size=self.size)

        self.WetWidget = WetherWidged(pos=(10 , 10), size=(450, 250), size_hint=(None, None))
        self.SmHome = SmartHomeDataWidget(pos=(470 , 10), size=(300, 380), size_hint=(None, None))


        self.clock = Label(text='[color=ffffff]22:30:38[/color]', markup = True, font_size=100, pos=(-410, 150) , font_name='fonts/hemi_head_bd_it.ttf')



        self.add_widget(self.background_image)
        self.add_widget(self.clock)
        self.add_widget(self.WetWidget)
        self.add_widget(self.SmHome)






class BoxApp(App):
    def build(self):
        dashboard = Dashboard()

        return dashboard
    def on_request_close(self, *args):
        print("end of programm")
        pass





if __name__ == '__main__':

    #AdcDataReader()

    BoxApp().run()
