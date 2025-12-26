#import kivy
#kivy.require('1.0.6')
#from glob import glob
#from os.path import join, dirname
#from kivy.app import App
#from kivy.logger import Logger
#from kivy.uix.scatter import Scatter
#from kivy.properties import StringProperty, ObjectProperty
#import sys
import datetime
import threading
import time
#import random
#from kivy.uix.boxlayout import BoxLayout
import requests
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
from kivy.properties import StringProperty, NumericProperty, BoundedNumericProperty
import subprocess
import time
from datetime import datetime, date, timedelta
from datetime import datetime
import json
#import custom_fun
import io , os, re, smbus # , i2c , psutil
#from kivy.uix.videoplayer import VideoPlayer
#from kivy_garden import graph
#import configparser
#import struct
from kivy.core.window import Window
from kivy.animation import Animation
#from math import sin
from kivy.uix.stencilview import StencilView
from kivy_garden.graph import Graph, MeshLinePlot, LinePlot, SmoothLinePlot
from kivy.factory import Factory

import configparser
import server
from udpService import UdpAsyncClient



Builder.load_file('kv/wet_widget.kv')
Builder.load_file('kv/io_ctrl.kv')
Builder.load_file('kv/SmartHomeWidget.kv')
Builder.load_file('kv/graph.kv')



config = configparser.ConfigParser()
config.read('config.ini')
WWO_CODE = {
    "113": "wic_clear_d.png",
    "116": "wic_cloudy.png",
    "119": "wic_rp_fog_mist.png",
    "122": "wic_rp_big_cloudy.png",
    "143": "wic_rp_fog_mist.png",
    "176": "wic_cloudy.png",
    "179": "wic_rp_hail.png",
    "182": "wic_rp_snow.png",
    "185": "wic_rp_snow.png",
    "200": "wic_rp_thunder.png",
    "227": "wic_snow.png",
    "230": "wic_snow.png",
    "248": "wic_rp_fog_mist.png",
    "260": "wic_rp_fog_mist.png",
    "263": "wic_rp_sleet.png",
    "266": "wic_rain_n.png",
    "281": "wic_sleet_n.png",
    "284": "wic_sleet_n.png",
    "293": "wic_rp_sleet.png",
    "296": "wic_rp_sleet.png",
    "299": "wic_rp_big_rain.png",
    "302": "wic_rp_big_rain.png",
    "305": "wic_rp_big_rain.png",
    "308": "wic_rp_big_rain.png",
    "311": "wic_sleet_n.png",
    "314": "wic_sleet_n.png",
    "317": "wic_sleet_n.png",
    "320": "wic_snow_n.png.png",
    "323": "wic_snow_n.png",
    "326": "wic_snow_n.png",
    "329": "wic_rp_big_rain.png",
    "332": "wic_rp_big_rain.png",
    "335": "wic_snow.png",
    "338": "wic_rp_big_rain.png",
    "350": "wic_sleet_n.png",
    "353": "wic_snow_n.png",
    "356": "wic_rp_big_rain.png",
    "359": "wic_rp_big_rain.png",
    "362": "wic_snow_n.png",
    "365": "wic_snow_n.png",
    "368": "wic_snow_n.png",
    "371": "wic_snow.png",
    "374": "wic_snow_n.png",
    "377": "wic_sleet_n.png",
    "386": "wic_thunder.png",
    "389": "wic_thunder.png",
    "392": "wic_rp_thunder.png",
    "395": "wic_rp_sleet.png",
}

tZone1 = int(-5)
tZone2 = int(-6)
tZone3 = int(-7)
tOutdoor = int(-8)
tBoiler = int(10)
BoilerCurrentMode = 'АВТО'
WaterHeaterCurrentMode = 'АВТО'
BoilerCurrentStat = 'ВКЛ'
WaterHeaterCurrentStat = 'ВКЛ'
WaterTankLevel = int(50)
WaterHeaterIndicator = 'images/grn_led.png'
WaterPressure = int(0)
kotelcurrentTemp = int(0)
WaterPressurePoints = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0), (30, 0), (31, 0), (32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0), (41, 0), (42, 0), (43, 0), (44, 0), (45, 0), (46, 0), (47, 0), (48, 0), (49, 0), (50, 0), (51, 0), (52, 0), (53, 0), (54, 0), (55, 0), (56, 0), (57, 0), (58, 0), (59, 0), (60, 0), (61, 0), (62, 0), (63, 0), (64, 0), (65, 0), (66, 0), (67, 0), (68, 0), (69, 0), (70, 0), (71, 0), (72, 0), (73, 0), (74, 0), (75, 0), (76, 0), (77, 0), (78, 0), (79, 0), (80, 0), (81, 0), (82, 0), (83, 0), (84, 0), (85, 0), (86, 0), (87, 0), (88, 0), (89, 0), (90, 0), (91, 0), (92, 0), (93, 0), (94, 0), (95, 0), (96, 0), (97, 0), (98, 0), (99, 0), (100, 0), (101, 0), (102, 0), (103, 0), (104, 0), (105, 0), (106, 0), (107, 0), (108, 0), (109, 0), (110, 0), (111, 0), (112, 0), (113, 0), (114, 0), (115, 0), (116, 0), (117, 0), (118, 0), (119, 0), (120, 0), (121, 0), (122, 0), (123, 0), (124, 0), (125, 0), (126, 0), (127, 0), (128, 0), (129, 0), (130, 0), (131, 0), (132, 0), (133, 0), (134, 0), (135, 0), (136, 0), (137, 0), (138, 0), (139, 0), (140, 0), (141, 0), (142, 0), (143, 0), (144, 0), (145, 0), (146, 0), (147, 0), (148, 0), (149, 0), (150, 0), (151, 0), (152, 0), (153, 0), (154, 0), (155, 0), (156, 0), (157, 0), (158, 0), (159, 0), (160, 0), (161, 0), (162, 0), (163, 0), (164, 0), (165, 0), (166, 0), (167, 0), (168, 0), (169, 0), (170, 0), (171, 0), (172, 0), (173, 0), (174, 0), (175, 0), (176, 0), (177, 0), (178, 0), (179, 0), (180, 0), (181, 0), (182, 0), (183, 0), (184, 0), (185, 0), (186, 0), (187, 0), (188, 0), (189, 0), (190, 0), (191, 0), (192, 0), (193, 0), (194, 0), (195, 0), (196, 0), (197, 0), (198, 0), (199, 0), (200, 0), (201, 0), (202, 0), (203, 0), (204, 0), (205, 0), (206, 0), (207, 0), (208, 0), (209, 0), (210, 0), (211, 0), (212, 0), (213, 0), (214, 0), (215, 0), (216, 0), (217, 0), (218, 0), (219, 0), (220, 0), (221, 0), (222, 0), (223, 0), (224, 0), (225, 0), (226, 0), (227, 0), (228, 0), (229, 0), (230, 0), (231, 0), (232, 0), (233, 0), (234, 0), (235, 0), (236, 0), (237, 0), (238, 0), (239, 0), (240, 0), (241, 0), (242, 0), (243, 0), (244, 0), (245, 0), (246, 0), (247, 0), (248, 0), (249, 0), (250, 0), (251, 0), (252, 0), (253, 0), (254, 0), (255, 0), (256, 0), (257, 0), (258, 0), (259, 0), (260, 0), (261, 0), (262, 0), (263, 0), (264, 0), (265, 0), (266, 0), (267, 0), (268, 0), (269, 0), (270, 0), (271, 0), (272, 0), (273, 0), (274, 0), (275, 0), (276, 0), (277, 0), (278, 0), (279, 0), (280, 0), (281, 0), (282, 0), (283, 0), (284, 0), (285, 0), (286, 0), (287, 0), (288, 0), (289, 0), (290, 0), (291, 0), (292, 0), (293, 0), (294, 0), (295, 0), (296, 0), (297, 0), (298, 0), (299, 0), (300, 0), (301, 0), (302, 0), (303, 0), (304, 0), (305, 0), (306, 0), (307, 0), (308, 0), (309, 0), (310, 0), (311, 0), (312, 0), (313, 0), (314, 0), (315, 0), (316, 0), (317, 0), (318, 0), (319, 0), (320, 0), (321, 0), (322, 0), (323, 0), (324, 0), (325, 0), (326, 0), (327, 0), (328, 0), (329, 0), (330, 0), (331, 0), (332, 0), (333, 0), (334, 0), (335, 0), (336, 0), (337, 0), (338, 0), (339, 0), (340, 0), (341, 0), (342, 0), (343, 0), (344, 0), (345, 0), (346, 0), (347, 0), (348, 0), (349, 0), (350, 0), (351, 0), (352, 0), (353, 0), (354, 0), (355, 0), (356, 0), (357, 0), (358, 0), (359, 0), (360, 0), (361, 0), (362, 0), (363, 0), (364, 0), (365, 0), (366, 0), (367, 0), (368, 0), (369, 0), (370, 0), (371, 0), (372, 0), (373, 0), (374, 0), (375, 0), (376, 0), (377, 0), (378, 0), (379, 0), (380, 0), (381, 0), (382, 0), (383, 0), (384, 0), (385, 0), (386, 0), (387, 0), (388, 0), (389, 0), (390, 0), (391, 0), (392, 0), (393, 0), (394, 0), (395, 0), (396, 0), (397, 0), (398, 0), (399, 0), (400, 0), (401, 0), (402, 0), (403, 0), (404, 0), (405, 0), (406, 0), (407, 0), (408, 0), (409, 0), (410, 0), (411, 0), (412, 0), (413, 0), (414, 0), (415, 0), (416, 0), (417, 0), (418, 0), (419, 0), (420, 0), (421, 0), (422, 0), (423, 0), (424, 0), (425, 0), (426, 0), (427, 0), (428, 0), (429, 0), (430, 0), (431, 0), (432, 0), (433, 0), (434, 0), (435, 0), (436, 0), (437, 0), (438, 0), (439, 0), (440, 0), (441, 0), (442, 0), (443, 0), (444, 0), (445, 0), (446, 0), (447, 0), (448, 0), (449, 0), (450, 0), (451, 0), (452, 0), (453, 0), (454, 0), (455, 0), (456, 0), (457, 0), (458, 0), (459, 0), (460, 0), (461, 0), (462, 0), (463, 0), (464, 0), (465, 0), (466, 0), (467, 0), (468, 0), (469, 0), (470, 0), (471, 0), (472, 0), (473, 0), (474, 0), (475, 0), (476, 0), (477, 0), (478, 0), (479, 0), (480, 0), (481, 0), (482, 0), (483, 0), (484, 0), (485, 0), (486, 0), (487, 0), (488, 0), (489, 0), (490, 0), (491, 0), (492, 0), (493, 0), (494, 0), (495, 0), (496, 0), (497, 0), (498, 0), (499, 0), (500, 0), (501, 0), (502, 0), (503, 0), (504, 0), (505, 0), (506, 0), (507, 0), (508, 0), (509, 0), (510, 0), (511, 0), (512, 0), (513, 0), (514, 0), (515, 0), (516, 0), (517, 0), (518, 0), (519, 0), (520, 0), (521, 0), (522, 0), (523, 0), (524, 0), (525, 0), (526, 0), (527, 0), (528, 0), (529, 0), (530, 0), (531, 0), (532, 0), (533, 0), (534, 0), (535, 0), (536, 0), (537, 0), (538, 0), (539, 0), (540, 0), (541, 0), (542, 0), (543, 0), (544, 0), (545, 0), (546, 0), (547, 0), (548, 0), (549, 0), (550, 0), (551, 0), (552, 0), (553, 0), (554, 0), (555, 0), (556, 0), (557, 0), (558, 0), (559, 0), (560, 0), (561, 0), (562, 0), (563, 0), (564, 0), (565, 0), (566, 0), (567, 0), (568, 0), (569, 0), (570, 0), (571, 0), (572, 0), (573, 0), (574, 0), (575, 0), (576, 0), (577, 0), (578, 0), (579, 0), (580, 0), (581, 0), (582, 0), (583, 0), (584, 0), (585, 0), (586, 0), (587, 0), (588, 0), (589, 0), (590, 0), (591, 0), (592, 0), (593, 0), (594, 0), (595, 0), (596, 0), (597, 0), (598, 0), (599, 0), (600, 0), (601, 0), (602, 0), (603, 0), (604, 0), (605, 0), (606, 0), (607, 0), (608, 0), (609, 0), (610, 0), (611, 0), (612, 0), (613, 0), (614, 0), (615, 0), (616, 0), (617, 0), (618, 0), (619, 0), (620, 0), (621, 0), (622, 0), (623, 0), (624, 0), (625, 0), (626, 0), (627, 0), (628, 0), (629, 0), (630, 0), (631, 0), (632, 0), (633, 0), (634, 0), (635, 0), (636, 0), (637, 0), (638, 0), (639, 0), (640, 0), (641, 0), (642, 0), (643, 0), (644, 0), (645, 0), (646, 0), (647, 0), (648, 0), (649, 0), (650, 0), (651, 0), (652, 0), (653, 0), (654, 0), (655, 0), (656, 0), (657, 0), (658, 0), (659, 0), (660, 0), (661, 0), (662, 0), (663, 0), (664, 0), (665, 0), (666, 0), (667, 0), (668, 0), (669, 0), (670, 0), (671, 0), (672, 0), (673, 0), (674, 0), (675, 0), (676, 0), (677, 0), (678, 0), (679, 0), (680, 0), (681, 0), (682, 0), (683, 0), (684, 0), (685, 0), (686, 0), (687, 0), (688, 0), (689, 0), (690, 0), (691, 0), (692, 0), (693, 0), (694, 0), (695, 0), (696, 0), (697, 0), (698, 0), (699, 0), (700, 0), (701, 0), (702, 0), (703, 0), (704, 0), (705, 0), (706, 0), (707, 0), (708, 0), (709, 0), (710, 0), (711, 0), (712, 0), (713, 0), (714, 0), (715, 0), (716, 0), (717, 0), (718, 0), (719, 0)]
KotelTempPoints = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0), (30, 0), (31, 0), (32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0), (41, 0), (42, 0), (43, 0), (44, 0), (45, 0), (46, 0), (47, 0), (48, 0), (49, 0), (50, 0), (51, 0), (52, 0), (53, 0), (54, 0), (55, 0), (56, 0), (57, 0), (58, 0), (59, 0), (60, 0), (61, 0), (62, 0), (63, 0), (64, 0), (65, 0), (66, 0), (67, 0), (68, 0), (69, 0), (70, 0), (71, 0), (72, 0), (73, 0), (74, 0), (75, 0), (76, 0), (77, 0), (78, 0), (79, 0), (80, 0), (81, 0), (82, 0), (83, 0), (84, 0), (85, 0), (86, 0), (87, 0), (88, 0), (89, 0), (90, 0), (91, 0), (92, 0), (93, 0), (94, 0), (95, 0), (96, 0), (97, 0), (98, 0), (99, 0), (100, 0), (101, 0), (102, 0), (103, 0), (104, 0), (105, 0), (106, 0), (107, 0), (108, 0), (109, 0), (110, 0), (111, 0), (112, 0), (113, 0), (114, 0), (115, 0), (116, 0), (117, 0), (118, 0), (119, 0), (120, 0), (121, 0), (122, 0), (123, 0), (124, 0), (125, 0), (126, 0), (127, 0), (128, 0), (129, 0), (130, 0), (131, 0), (132, 0), (133, 0), (134, 0), (135, 0), (136, 0), (137, 0), (138, 0), (139, 0), (140, 0), (141, 0), (142, 0), (143, 0), (144, 0), (145, 0), (146, 0), (147, 0), (148, 0), (149, 0), (150, 0), (151, 0), (152, 0), (153, 0), (154, 0), (155, 0), (156, 0), (157, 0), (158, 0), (159, 0), (160, 0), (161, 0), (162, 0), (163, 0), (164, 0), (165, 0), (166, 0), (167, 0), (168, 0), (169, 0), (170, 0), (171, 0), (172, 0), (173, 0), (174, 0), (175, 0), (176, 0), (177, 0), (178, 0), (179, 0), (180, 0), (181, 0), (182, 0), (183, 0), (184, 0), (185, 0), (186, 0), (187, 0), (188, 0), (189, 0), (190, 0), (191, 0), (192, 0), (193, 0), (194, 0), (195, 0), (196, 0), (197, 0), (198, 0), (199, 0), (200, 0), (201, 0), (202, 0), (203, 0), (204, 0), (205, 0), (206, 0), (207, 0), (208, 0), (209, 0), (210, 0), (211, 0), (212, 0), (213, 0), (214, 0), (215, 0), (216, 0), (217, 0), (218, 0), (219, 0), (220, 0), (221, 0), (222, 0), (223, 0), (224, 0), (225, 0), (226, 0), (227, 0), (228, 0), (229, 0), (230, 0), (231, 0), (232, 0), (233, 0), (234, 0), (235, 0), (236, 0), (237, 0), (238, 0), (239, 0), (240, 0), (241, 0), (242, 0), (243, 0), (244, 0), (245, 0), (246, 0), (247, 0), (248, 0), (249, 0), (250, 0), (251, 0), (252, 0), (253, 0), (254, 0), (255, 0), (256, 0), (257, 0), (258, 0), (259, 0), (260, 0), (261, 0), (262, 0), (263, 0), (264, 0), (265, 0), (266, 0), (267, 0), (268, 0), (269, 0), (270, 0), (271, 0), (272, 0), (273, 0), (274, 0), (275, 0), (276, 0), (277, 0), (278, 0), (279, 0), (280, 0), (281, 0), (282, 0), (283, 0), (284, 0), (285, 0), (286, 0), (287, 0), (288, 0), (289, 0), (290, 0), (291, 0), (292, 0), (293, 0), (294, 0), (295, 0), (296, 0), (297, 0), (298, 0), (299, 0), (300, 0), (301, 0), (302, 0), (303, 0), (304, 0), (305, 0), (306, 0), (307, 0), (308, 0), (309, 0), (310, 0), (311, 0), (312, 0), (313, 0), (314, 0), (315, 0), (316, 0), (317, 0), (318, 0), (319, 0), (320, 0), (321, 0), (322, 0), (323, 0), (324, 0), (325, 0), (326, 0), (327, 0), (328, 0), (329, 0), (330, 0), (331, 0), (332, 0), (333, 0), (334, 0), (335, 0), (336, 0), (337, 0), (338, 0), (339, 0), (340, 0), (341, 0), (342, 0), (343, 0), (344, 0), (345, 0), (346, 0), (347, 0), (348, 0), (349, 0), (350, 0), (351, 0), (352, 0), (353, 0), (354, 0), (355, 0), (356, 0), (357, 0), (358, 0), (359, 0), (360, 0), (361, 0), (362, 0), (363, 0), (364, 0), (365, 0), (366, 0), (367, 0), (368, 0), (369, 0), (370, 0), (371, 0), (372, 0), (373, 0), (374, 0), (375, 0), (376, 0), (377, 0), (378, 0), (379, 0), (380, 0), (381, 0), (382, 0), (383, 0), (384, 0), (385, 0), (386, 0), (387, 0), (388, 0), (389, 0), (390, 0), (391, 0), (392, 0), (393, 0), (394, 0), (395, 0), (396, 0), (397, 0), (398, 0), (399, 0), (400, 0), (401, 0), (402, 0), (403, 0), (404, 0), (405, 0), (406, 0), (407, 0), (408, 0), (409, 0), (410, 0), (411, 0), (412, 0), (413, 0), (414, 0), (415, 0), (416, 0), (417, 0), (418, 0), (419, 0), (420, 0), (421, 0), (422, 0), (423, 0), (424, 0), (425, 0), (426, 0), (427, 0), (428, 0), (429, 0), (430, 0), (431, 0), (432, 0), (433, 0), (434, 0), (435, 0), (436, 0), (437, 0), (438, 0), (439, 0), (440, 0), (441, 0), (442, 0), (443, 0), (444, 0), (445, 0), (446, 0), (447, 0), (448, 0), (449, 0), (450, 0), (451, 0), (452, 0), (453, 0), (454, 0), (455, 0), (456, 0), (457, 0), (458, 0), (459, 0), (460, 0), (461, 0), (462, 0), (463, 0), (464, 0), (465, 0), (466, 0), (467, 0), (468, 0), (469, 0), (470, 0), (471, 0), (472, 0), (473, 0), (474, 0), (475, 0), (476, 0), (477, 0), (478, 0), (479, 0), (480, 0), (481, 0), (482, 0), (483, 0), (484, 0), (485, 0), (486, 0), (487, 0), (488, 0), (489, 0), (490, 0), (491, 0), (492, 0), (493, 0), (494, 0), (495, 0), (496, 0), (497, 0), (498, 0), (499, 0), (500, 0), (501, 0), (502, 0), (503, 0), (504, 0), (505, 0), (506, 0), (507, 0), (508, 0), (509, 0), (510, 0), (511, 0), (512, 0), (513, 0), (514, 0), (515, 0), (516, 0), (517, 0), (518, 0), (519, 0), (520, 0), (521, 0), (522, 0), (523, 0), (524, 0), (525, 0), (526, 0), (527, 0), (528, 0), (529, 0), (530, 0), (531, 0), (532, 0), (533, 0), (534, 0), (535, 0), (536, 0), (537, 0), (538, 0), (539, 0), (540, 0), (541, 0), (542, 0), (543, 0), (544, 0), (545, 0), (546, 0), (547, 0), (548, 0), (549, 0), (550, 0), (551, 0), (552, 0), (553, 0), (554, 0), (555, 0), (556, 0), (557, 0), (558, 0), (559, 0), (560, 0), (561, 0), (562, 0), (563, 0), (564, 0), (565, 0), (566, 0), (567, 0), (568, 0), (569, 0), (570, 0), (571, 0), (572, 0), (573, 0), (574, 0), (575, 0), (576, 0), (577, 0), (578, 0), (579, 0), (580, 0), (581, 0), (582, 0), (583, 0), (584, 0), (585, 0), (586, 0), (587, 0), (588, 0), (589, 0), (590, 0), (591, 0), (592, 0), (593, 0), (594, 0), (595, 0), (596, 0), (597, 0), (598, 0), (599, 0), (600, 0), (601, 0), (602, 0), (603, 0), (604, 0), (605, 0), (606, 0), (607, 0), (608, 0), (609, 0), (610, 0), (611, 0), (612, 0), (613, 0), (614, 0), (615, 0), (616, 0), (617, 0), (618, 0), (619, 0), (620, 0), (621, 0), (622, 0), (623, 0), (624, 0), (625, 0), (626, 0), (627, 0), (628, 0), (629, 0), (630, 0), (631, 0), (632, 0), (633, 0), (634, 0), (635, 0), (636, 0), (637, 0), (638, 0), (639, 0), (640, 0), (641, 0), (642, 0), (643, 0), (644, 0), (645, 0), (646, 0), (647, 0), (648, 0), (649, 0), (650, 0), (651, 0), (652, 0), (653, 0), (654, 0), (655, 0), (656, 0), (657, 0), (658, 0), (659, 0), (660, 0), (661, 0), (662, 0), (663, 0), (664, 0), (665, 0), (666, 0), (667, 0), (668, 0), (669, 0), (670, 0), (671, 0), (672, 0), (673, 0), (674, 0), (675, 0), (676, 0), (677, 0), (678, 0), (679, 0), (680, 0), (681, 0), (682, 0), (683, 0), (684, 0), (685, 0), (686, 0), (687, 0), (688, 0), (689, 0), (690, 0), (691, 0), (692, 0), (693, 0), (694, 0), (695, 0), (696, 0), (697, 0), (698, 0), (699, 0), (700, 0), (701, 0), (702, 0), (703, 0), (704, 0), (705, 0), (706, 0), (707, 0), (708, 0), (709, 0), (710, 0), (711, 0), (712, 0), (713, 0), (714, 0), (715, 0), (716, 0), (717, 0), (718, 0), (719, 0)]

TmpPressurePoints = []
TmpKotelTempPoints = []

Current_Condition = [ '0' , '1' , '2' , 'WetIcons/wic_snow_n.png' , '---']
Tommorow_Condition_Slot1 = [ '--' , 'WetIcons/wic_rp_unknow.png']
Tommorow_Condition_Slot2 = [ '--' , 'WetIcons/wic_rp_unknow.png']
Tommorow_Condition_Slot3 = [ '--' , 'WetIcons/wic_rp_unknow.png']
Tommorow_Condition_Slot4 = [ '--' , 'WetIcons/wic_rp_unknow.png']

boiler_en = False
g_kotel = False
g_spare = False

shell_str=subprocess.check_output(["lscpu | grep 'Model name' | cut -f 2 -d ':' | awk '{$1=$1}1'"] , shell=True)
shell_str=shell_str.decode('utf-8')
if(shell_str.find('Intel(R)')!=-1):
    print (shell_str)
    Window.size = (1280, 400)




class SmartHomeDataWidget(Screen):
    HouseTemperatureStr = StringProperty('Дитяча:       ---С')
    BoilerTemperatureStr = StringProperty('Т Двір:         ---С\nТ Котла:     ---С')
    #WaterHeaterStr = StringProperty('Бойлер:              ВКЛ\nРежим:              АВТО')
    led_icon = StringProperty('images/grn_led.png')
    
    energyColorFrame = StringProperty('images/EN_ERR.png')
    acVoltage = StringProperty("220,220,220 V")
    acTotalPower = StringProperty("758 W")
    socValue     = StringProperty("--- %")
    socCurrent     = StringProperty("XX A")


class GraphWidget(Scatter):
    GraphPlot = StringProperty(WaterPressurePoints)
    UnitY = StringProperty("none")
    UnitX = StringProperty("none")
    MaxX = StringProperty(720)
    MaxY = StringProperty(6)
    MinX = StringProperty(0)
    MinY = StringProperty(0)
    xTicksMinor = StringProperty(7)
    xTicksMajro = StringProperty(60)
    
    pass

class WetherWidged(Screen):
    CurrentWet = StringProperty("Температура:    +31С \nВидимість:          10Км\nМісцями дощ \nВітер:                 10Км/г")
    CurrentWetIcon = StringProperty('WetIcons/wic_snow_n.png')
    Tommorow1 = StringProperty('WetIcons/wic_rp_unknow.png')
    Tommorow2 = StringProperty('WetIcons/wic_rp_unknow.png')
    Tommorow3 = StringProperty('WetIcons/wic_rp_unknow.png')
    Tommorow4 = StringProperty('WetIcons/wic_rp_unknow.png')

    TommorowT1 = StringProperty('--°C')
    TommorowT2 = StringProperty('--°C')
    TommorowT3 = StringProperty('--°C')
    TommorowT4 = StringProperty('--°C')
    pass


class IoControll(Screen):
    def io_swich(self, swichId, featureState):
        user_key = "key" 
        url = f"http://192.168.1.5:8000/setSwitchById/?switch_id={swichId}&state={featureState}&userKey={user_key}"
        try:
            response = requests.get(url, headers={'accept': 'application/json'}, timeout=3)
            if response.status_code == 200:
                print(response.json())
            else:
                print("Switch set error:", response.status_code)
        except Exception as e:
            print("Switch set exception:", e)



class Dashboard(FloatLayout):
    tim = int(0)
    acSource = ""
    report_data = []
    def __init__(self, **kwargs):
        Server_handler()
        self.udpClient = UdpAsyncClient(self, self.serverUdpIncomingData, 5005)
        self.udpClient = UdpAsyncClient(self, self.batteryUdpIncomingData, 5006)


        global WaterPressurePoints
        self.WaterPressurePlot = LinePlot(line_width=2, color=[57 / 255, 255 / 255, 150 / 255, 255 / 255])
        self.WaterHeaterPlot = LinePlot(line_width=2, color=[240 / 255, 137 / 255, 19 / 255, 255 / 255])
        
        super(Dashboard, self).__init__(**kwargs)
        self.background_image = Image(source='images/bg_1.png', size=self.size)

        self.WetWidget = WetherWidged(pos=(10 , 10), size=(450, 250), size_hint=(None, None))
        self.SmHome = SmartHomeDataWidget(pos=(470 , 10), size=(300, 380), size_hint=(None, None))

        self.IoCtrl = IoControll(pos=(800 , 225), size=(400, 170), size_hint=(None, None))

        self.clock = Label(text='[color=ffffff]22:30:38[/color]', markup = True, font_size=100, pos=(-410, 150) , font_name='fonts/hemi_head_bd_it.ttf')

        self.ip = Label(text='[color=ffffff]192.168.1.200[/color]', markup=True, font_size=18, pos=(250, -190),
                           font_name='fonts/hemi_head_bd_it.ttf')

        #self.add_widget(self.background_image)
        self.add_widget(self.clock)
        self.add_widget(self.ip)
        self.add_widget(self.WetWidget)
        self.add_widget(self.SmHome)
        self.add_widget(self.IoCtrl)

        myIP = subprocess.check_output(["./getIP.sh"]).decode('utf-8')
        self.ip.text = myIP
        
        self.water_t = water_tank(do_rotation=False, do_scale=False, do_translation=False, value=0, pos=(480, 15))
        self.add_widget(self.water_t)

        self.analog_display = analog_meter(do_rotation=False, do_scale=False, do_translation=False, value=0, pos=(603, 70))
        self.add_widget(self.analog_display)

        self.WaterPressureGraph = GraphWidget(pos=(775, 40), size=(250, 170), size_hint=(None, None), do_rotation=False,
                                     do_scale=False, do_translation=False)
        self.WaterPressureGraph.UnitY = "MPA/10"
        self.WaterPressureGraph.UnitX = "Тиск за 12 годин"
        self.WaterPressureGraph.MaxX = "720"
        self.WaterPressureGraph.MaxX = "6"


        self.WaterHeaterTemp = GraphWidget(pos=(1030, 40), size=(250, 170), size_hint=(None, None), do_rotation=False,
                                     do_scale=False, do_translation=False)
        self.WaterHeaterTemp.UnitY = "t°C"
        self.WaterHeaterTemp.UnitX = "Котел за 12 годин"
        self.WaterHeaterTemp.MaxY = "7"
        self.WaterHeaterTemp.MinY = "3"


        
        self.add_widget(self.WaterPressureGraph)
        self.add_widget(self.WaterHeaterTemp)



        #self.WaterPressureGraph.GraphPlot = self.WaterPressurePlot



        Clock.schedule_interval(lambda dt: self.update_time(), 1)
        Clock.schedule_interval(lambda dt: self.on_minut_event(), 60)


    def on_minut_event(self):
        global WaterPressurePoints
        global TmpPressurePoints
        global KotelTempPoints
        global TmpKotelTempPoints
        
        #kotelcurrentTemp
        self.i = 0
        myIP = subprocess.check_output(["./getIP.sh"]).decode('utf-8')
        self.ip.text=myIP
        for x in range(720):
            if x != 0:
                TmpPressurePoints.append((self.i, WaterPressurePoints[x][1]))
                TmpKotelTempPoints.append((self.i, KotelTempPoints[x][1]))
                self.i += 1
        TmpPressurePoints.append((719, WaterPressure / 100))
        TmpKotelTempPoints.append((719, float(tBoiler) / 10))
        WaterPressurePoints = []
        KotelTempPoints = []
        WaterPressurePoints = TmpPressurePoints
        KotelTempPoints = TmpKotelTempPoints
        TmpPressurePoints = []
        TmpKotelTempPoints = []

    def serverUdpIncomingData(self, data):
        try:
            self.SmHome.acVoltage = str(data['voltage']).replace("[", "").replace("]", "") + " V"
            self.SmHome.acTotalPower = f"{data['total_power']} W"
            self.acSource = data['source']
            #print(data)
        except:
            self.SmHome.acVoltage = "[color=ff0000]ERROR[/color]"
            self.SmHome.acTotalPower = "[color=ff0000]ERROR[/color]"
            self.acSource = "err"
        
    def batteryUdpIncomingData(self, data):
        #print(data)
        socLevelColor = "00ff00"
        socCurrentColor = "20ff20"
        try:
            if(data['socStatusLoad'][0] <= 80):
                socLevelColor = "ffff00"
            if(data['socStatusLoad'][0] <= 60):
                socLevelColor = "ff0000"

            if((data['socCurrent']/10) <= -1):
                socCurrentColor = "ffff00"
            if((data['socCurrent']/10) >= 1):
                socCurrentColor = "8080ff"

            self.SmHome.socValue = f"[color={socLevelColor}]{data['socStatusLoad'][0]} %[/color]"
            self.SmHome.socCurrent = f"[color={socCurrentColor}]{data['socCurrent']/10}A {data['socVoltage']/100} V[/color] {int(data['socTemperature']/10)}C"  
            #; 
            #print(data)
        except:
            self.SmHome.socValue ="[color=ff0000]ERROR[/color]"
            self.SmHome.socCurrent = "[color=ff0000]ERROR[/color]"
            
    def get_switches_status(self):
        try:
            response = requests.get(
                'http://192.168.1.5:8000/getSwitches/',
                headers={'accept': 'application/json'},
                timeout=3
            )
            if response.status_code == 200:
                switches = response.json().get("ok", [])
                # Десеріалізуємо у словник для зручного доступу
                switches_dict = {sw['switch_name']: sw for sw in switches}
                # Отримати потрібні параметри:
                water_heater_manual = switches_dict.get("WaterHeaterManual", {})
                water_heater_power = switches_dict.get("WaterHeaterPower", {})
                # Приклад доступу до state:
                manual_state = water_heater_manual.get("state", None)
                power_state = water_heater_power.get("state", None)
                # Можна повертати весь словник для подальшої роботи
                return switches_dict
            else:
                print("Switches API error:", response.status_code)
                return {}
        except Exception as e:
            print("Switches API exception:", e)
            return {}

    def update_time(self):
        #server.Server_handler_second.data_transfer(self, {'x': "aaa",'y': "bbb"})
        try:
            #print(threading.enumerate()[1].is_alive())
            if threading.enumerate()[1].is_alive() != True:
                Server_handler()
                
                f = open("log.txt", "a")
                f.write('AUTO Run SRV handler   -  ' + datetime.now().strftime('%d/%m/%Y-%H:%M:%S') + '\n')
                f.close()



        except:
            Server_handler()
            f = open("log.txt", "a")
            f.write('AUTO Run SRV handler after crash   -  ' + datetime.now().strftime('%d/%m/%Y-%H:%M:%S') + '\n')
            f.close()
        switches = self.get_switches_status()
        water_heater_manual_state = switches.get("WaterHeaterManual", {}).get("state")
        water_heater_power_state = switches.get("WaterHeaterPower", {}).get("state")   
        #if g_kotel == True:
        #    self.IoCtrl.ids.kotel_led.source = 'images/led_on_g.png'
        #    self.IoCtrl.ids.g_kotel_sw.active = True
        #else:
        #    self.IoCtrl.ids.kotel_led.source = 'images/led_off_g.png'
        #    self.IoCtrl.ids.g_kotel_sw.active = False
        if water_heater_manual_state:
            self.IoCtrl.ids.w_heater_sw.active = True
        else:
            self.IoCtrl.ids.w_heater_sw.active = False

        if water_heater_power_state == True or water_heater_manual_state == True:
            self.IoCtrl.ids.boiler_led.source = 'images/led_on_g.png'
        #    self.IoCtrl.ids.w_heater_sw.active = True
        else:
            self.IoCtrl.ids.boiler_led.source = 'images/led_off_g.png'
        #    self.IoCtrl.ids.w_heater_sw.active = False

        


        self.WaterPressurePlot.points = WaterPressurePoints
        self.WaterPressureGraph.ids.graph_data.add_plot(self.WaterPressurePlot)

        self.WaterHeaterPlot.points = KotelTempPoints
        self.WaterHeaterTemp.ids.graph_data.add_plot(self.WaterHeaterPlot)

        self.clock.text='[color=21BCFF]'+datetime.now().strftime('%H:%M:%S')+'[/color]'
        self.tim += 1
        self.SmHome.HouseTemperatureStr = 'Дитяча:       ' + str(tZone2) + '°С'
        self.SmHome.BoilerTemperatureStr = 'Т Двір:         ' + str(tOutdoor) + '°С\nТ Котла:     '+str(tBoiler) + '°С'
        
        
        #self.SmHome.WaterHeaterStr = 'Бойлер:              ' + WaterHeaterCurrentStat + '\nРежим:              ' + WaterHeaterCurrentMode
        self.water_t.value = WaterTankLevel
        self.SmHome.led_icon = WaterHeaterIndicator
        
        
        self.WetWidget.CurrentWet = "Температура:    " + Current_Condition[0] + "°С \nВидимість:          " + Current_Condition[1] + "Км\n" + Current_Condition[4] + " \nВітер:                 " + Current_Condition[2] + "Км/г"
        self.WetWidget.CurrentWetIcon = Current_Condition[3]
        self.WetWidget.TommorowT1 = Tommorow_Condition_Slot1[0] + '°C'
        self.WetWidget.Tommorow1 = Tommorow_Condition_Slot1[1]
        self.WetWidget.TommorowT2 = Tommorow_Condition_Slot2[0] + '°C'
        self.WetWidget.Tommorow2 = Tommorow_Condition_Slot2[1]
        self.WetWidget.TommorowT3 = Tommorow_Condition_Slot3[0] + '°C'
        self.WetWidget.Tommorow3 = Tommorow_Condition_Slot3[1]
        self.WetWidget.TommorowT4 = Tommorow_Condition_Slot4[0] + '°C'
        self.WetWidget.Tommorow4 = Tommorow_Condition_Slot4[1]
        self.analog_display.value = WaterPressure
        
        if(self.acSource == "AC"):
            self.SmHome.energyColorFrame = 'images/EN_OK.png'
        elif(self.acSource == "err"):
            self.SmHome.energyColorFrame = 'images/EN_ERR.png'    
        else:
            self.SmHome.energyColorFrame = 'images/EN_NOK.png' 

        if (self.tim >= 100):
            self.tim = 0


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

        lcd_bg = Image(source='images/lcd_bg.png', size=(150, 50), pos=(0, -55))
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
            size=(110, 160),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )
        water_tank_bar_empty = StencilView(size_hint=(None, None), size=(110, 160), pos=(0, 0))
        water_tank_empty_img = Image(source='images/water_empty.png', size=(110, 160), pos=(0, 0))
        water_tank_bar_empty.add_widget(water_tank_empty_img)
        self._tank.add_widget(water_tank_bar_empty)
        self.water_tank_bar = StencilView(size_hint=(None, None), size=(110, 160), pos=(0, 0))
        water_tank_full_img = Image(source='images/water_full.png', size=(110, 160), pos=(0, 0))
        self.water_tank_bar.add_widget(water_tank_full_img)
        self._tank.add_widget(self.water_tank_bar)
        self.water_tank_bar.height = self.value
        self.percent_lbl=Label(text='100%', font_name='fonts/hemi_head_bd_it.ttf', halign="center", text_size=self.size, font_size=32, pos=(5, 50), markup=True)
        self._tank.add_widget(self.percent_lbl)
        self.add_widget(self._tank)

    def _update(self, *args):
        self.text_color = 'ffffff'
        if (self.value <= 20):
            self.text_color = 'ff0000'
        self.percent_lbl.text='[color='+ self.text_color +']' + str(self.value) + '%[/color]'
        self.water_tank_bar.height = self.value+10


class Server_handler(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global tOutdoor
        global tZone1
        global tZone2
        global tZone3
        global tBoiler
        global WaterTankLevel
        global WaterHeaterIndicator
        global WaterPressure
        global Current_Condition
        global Tommorow_Condition_Slot1
        global Tommorow_Condition_Slot2
        global Tommorow_Condition_Slot3
        global Tommorow_Condition_Slot4
        global boiler_en
        global g_kotel
        global g_spare
        wttr_req = 0
        if (config['server']['enable'] == "true"):
            print("http enable")
            while True:
                server_str_request = "http://" + config['server']['url'] + ":" + config['server']['port'] + "/" + \
                                     config['server']['script']

                try:
                    response = requests.get(server_str_request)
                    if (response.status_code == 200):
                        result = response.content.decode('utf-8')
                        if (result.find('smMonitor/n') != -1):
                            self.parse_SM(result.split("/"))
                except:
                    f = open("log.txt", "a")
                    f.write('SmarHome server error  -  ' + datetime.now().strftime('%d/%m/%Y-%H:%M:%S') + '\n')
                    f.close()
                    print('SmarHome server error')
                if wttr_req == 0:
                    try:
                        response = requests.get('http://wttr.in/Svalyava?format=j1&lang=ru')
                        if (response.status_code == 200):
                            self.parse_wether(response)

                    except:
                        f = open("log.txt", "a")
                        f.write('Wether server error  -  ' + datetime.now().strftime('%d/%m/%Y-%H:%M:%S') + '\n')
                        f.close()
                        print('Wether server error')

                try:
                    io_stat = requests.get('http://192.168.1.5/sm/io_ctrl.php?fn=read&key=0XlCqivBS8rHa5Q0YIF4o9yqpTmyasU4', auth=("vanyap1", 'vanyap198808'))
                    if (io_stat.status_code == 200):
                        #self.parse_wether(response)
                        precheck_arr = io_stat.text.split(":")
                        #print(precheck_arr[2])
                        if (precheck_arr[0]=='data' and precheck_arr[5]=='end'):
                            if precheck_arr[4] == '1':
                                boiler_en = True
                            else:
                                boiler_en = False
                            if precheck_arr[3] == '1':
                                g_kotel = True
                            else:
                                g_kotel = False
                            if precheck_arr[2] == '1':
                                g_spare = True
                            else:
                                g_spare = False

                        pass
                except:
                    f = open("log.txt", "a")
                    f.write('IO ctrl error  -  ' + datetime.now().strftime('%d/%m/%Y-%H:%M:%S') + '\n')
                    f.close()
                    print('kotel_parser_error')
                if wttr_req >= 720 :
                    wttr_req = 0
                else:
                    wttr_req +=1



                #print(json.dumps(ess_dict, indent=4))
                time.sleep(5)
    def parse_wether(self, arg):
        global Current_Condition
        global Tommorow_Condition_Slot1
        global Tommorow_Condition_Slot2
        global Tommorow_Condition_Slot3
        global Tommorow_Condition_Slot4
        ess_dict = json.loads(arg.content.decode('utf-8'))
        Current_Condition[0] = ess_dict['current_condition'][0]['temp_C']
        Current_Condition[1] = ess_dict['current_condition'][0]['visibility']
        Current_Condition[2] = ess_dict['current_condition'][0]['windspeedKmph']
        Current_Condition[3] = 'WetIcons/' + WWO_CODE[ess_dict['current_condition'][0]['weatherCode']]
        Current_Condition[4] = ess_dict['current_condition'][0]['lang_ru'][0]['value']
        Tommorow_Condition_Slot1[0] = ess_dict['weather'][1]['hourly'][3]['tempC']
        Tommorow_Condition_Slot1[1] = 'WetIcons/' + WWO_CODE[ess_dict['weather'][1]['hourly'][3]['weatherCode']]
        Tommorow_Condition_Slot2[0] = ess_dict['weather'][1]['hourly'][4]['tempC']
        Tommorow_Condition_Slot2[1] = 'WetIcons/' + WWO_CODE[ess_dict['weather'][1]['hourly'][4]['weatherCode']]
        Tommorow_Condition_Slot3[0] = ess_dict['weather'][1]['hourly'][6]['tempC']
        Tommorow_Condition_Slot3[1] = 'WetIcons/' + WWO_CODE[ess_dict['weather'][1]['hourly'][6]['weatherCode']]
        Tommorow_Condition_Slot4[0] = ess_dict['weather'][1]['hourly'][7]['tempC']
        Tommorow_Condition_Slot4[1] = 'WetIcons/' + WWO_CODE[ess_dict['weather'][1]['hourly'][7]['weatherCode']]
    def parse_SM(self, arg):
        global tOutdoor
        global tZone1
        global tZone2
        global tZone3
        global tBoiler
        global WaterTankLevel
        global WaterHeaterIndicator
        global WaterPressure
        if (len(arg) == 15):
            tOutdoor = arg[2]
            tBoiler = arg[3]
            tZone1 = arg[3]
            tZone2 = arg[5]
            tZone3 = arg[6]
            WaterPressure = int(arg[12])
            if (arg[4] == '1'):
                WaterHeaterIndicator = 'images/grn_led.png'
            else:
                WaterHeaterIndicator = 'images/grey_led.png'
            WaterTankLevel = int(arg[13])-128

class BoxApp(App):
    def build(self):
        dashboard = Dashboard()
        #server.Server_handler_task()
        return dashboard
    def on_request_close(self, *args):
        print("end of programm")
        pass





if __name__ == '__main__':

    #AdcDataReader()

    BoxApp().run()

